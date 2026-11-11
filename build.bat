@echo off
echo ============================================
echo  Building Trisakra Transcript Studio (.exe)
echo ============================================
python -m pip install pyinstaller
python -m pip install -r requirements.txt
python -m PyInstaller --noconfirm --onedir --windowed --icon "assets\icon.ico" --add-data "assets;assets" --name "Trisakra Transcript Studio" --collect-all faster_whisper --collect-all ctranslate2 --collect-all av --collect-all onnxruntime app.py
echo.
echo Done. Your app is in the "dist\Trisakra Transcript Studio" folder.
echo Double-click "Trisakra Transcript Studio.exe" inside it to test.
pause
