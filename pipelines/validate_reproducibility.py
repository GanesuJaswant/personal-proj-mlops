import os
import sys

# Reference execution from src
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src_dir = os.path.join(base_dir, 'src')
sys.path.append(src_dir)

from validate_reproducibility import run_deterministic_test

if __name__ == "__main__":
    success = run_deterministic_test()
    if not success:
        sys.exit(1)
