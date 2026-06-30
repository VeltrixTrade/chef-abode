import os, sys, json, asyncio, uuid
from pathlib import Path
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

# Add TradingAgents to path
sys.path.insert(0, str(Path("C:/Users/MustafaMerany/Desktop/TradingAgents").resolve()))

# Load .env from TradingAgents
from dotenv import load_dotenv
load_dotenv(Path("C:/Users/MustafaMerany/Desktop/TradingAgents/.env"))

analysis_results = {}

app = FastAPI(title="TradingView Analyzer")

@app.get("/", response_class=HTMLResponse)
async def index():
    path = Path(__file__).parent / "templates" / "index.html"
    return HTMLResponse(content=path.read_text(encoding="utf-8"))

@app.post("/analyze")
async def analyze(
    ticker: str = Query(...),
    llm_provider: str = Query("google"),
):
    task_id = uuid.uuid4().hex[:8]
    analysis_results[task_id] = {"status": "running", "result": None}

    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, _run_task, task_id, ticker, llm_provider)

    return JSONResponse({"task_id": task_id, "status": "running"})

@app.get("/result/{task_id}")
async def get_result(task_id: str):
    data = analysis_results.get(task_id, {"status": "not_found", "result": None})
    return JSONResponse(data)

def _run_task(task_id: str, ticker: str, llm_provider: str):
    try:
        from tradingagents.graph.trading_graph import TradingAgentsGraph
        from tradingagents.default_config import DEFAULT_CONFIG

        config = DEFAULT_CONFIG.copy()
        config["llm_provider"] = llm_provider

        ta = TradingAgentsGraph(debug=False, config=config)
        _, decision = ta.propagate(ticker)

        analysis_results[task_id] = {"status": "done", "result": decision}
    except Exception as e:
        analysis_results[task_id] = {"status": "error", "result": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
