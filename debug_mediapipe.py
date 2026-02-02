import sys
import os
import importlib.util

print(f"Python executable: {sys.executable}")
try:
    import mediapipe
    mp_path = os.path.dirname(mediapipe.__file__)
    print(f"MediaPipe path: {mp_path}")
    
    solutions_path = os.path.join(mp_path, 'solutions')
    if os.path.exists(solutions_path):
        print(f"Directory 'solutions' FOUND at: {solutions_path}")
        print(f"Contents: {os.listdir(solutions_path)}")
        
        # Check for __init__.py
        init_file = os.path.join(solutions_path, '__init__.py')
        if os.path.exists(init_file):
             print("'solutions/__init__.py' exists.")
        else:
             print("'solutions/__init__.py' MISSING.")

    else:
        print(f"Directory 'solutions' NOT FOUND at: {solutions_path}")
        print("This indicates a corrupted or incomplete installation.")

except ImportError as e:
    print(f"ImportError: {e}")
except Exception as e:
    print(f"Error: {e}")
