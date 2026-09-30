import os
import sys

# Reference execution from src
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src_dir = os.path.join(base_dir, 'src')
sys.path.append(src_dir)

from preprocess_pipeline import run_preprocessing

if __name__ == "__main__":
    run_preprocessing()
