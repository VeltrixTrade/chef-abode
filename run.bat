@echo off
cd /d "C:\Users\MustafaMerany\Desktop\TradingViewAnalyzer"
call "C:\Users\MustafaMerany\Desktop\TradingAgents\.venv\Scripts\activate.bat"
echo ✅ TradingView Analyzer
echo.
echo 🔹 افتح المتصفح على: http://127.0.0.1:8000
echo 🔹 اضغط Ctrl+C للإيقاف
echo.
python server.py
pause
