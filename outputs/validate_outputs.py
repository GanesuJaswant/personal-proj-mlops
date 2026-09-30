import os
import sys

# Reference execution from src
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src_dir = os.path.join(base_dir, 'src')
sys.path.append(src_dir)

from validate_outputs import validate_preprocessing_outputs

if __name__ == "__main__":
    success = validate_preprocessing_outputs()
    if not success:
        sys.exit(1)
