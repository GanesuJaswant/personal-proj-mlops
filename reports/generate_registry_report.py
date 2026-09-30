import os
import sys

# Reference execution from src
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src_dir = os.path.join(base_dir, 'src')
sys.path.append(src_dir)

from generate_registry_report import generate_registry_report

if __name__ == "__main__":
    success = generate_registry_report()
    if not success:
        sys.exit(1)
