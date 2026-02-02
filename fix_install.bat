@echo off
echo ==========================================
echo FIXING MEDIAPIPE INSTALLATION
echo ==========================================

echo [1/4] Uninstalling current mediapipe...
pip uninstall -y mediapipe

echo [2/4] Clearing pip cache to remove broken files...
pip cache purge

echo [3/4] Installing a stable version of MediaPipe (0.10.9)...
pip install mediapipe==0.10.9 --no-cache-dir

echo [4/4] Ensuring other requirements are met...
pip install -r requirements.txt

echo ==========================================
echo DONE! Please try running python main.py now.
echo ==========================================
pause
