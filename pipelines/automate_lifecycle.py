import os
import sys

# Reference execution from src
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src_dir = os.path.join(base_dir, 'src')
sys.path.append(src_dir)

from automate_lifecycle import automate_champion_challenger

if __name__ == "__main__":
    automate_champion_challenger()
