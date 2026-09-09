"""
Legacy Wrapper: generate_presentation.py
Forwarding execution to modular src.reporting.presentation.
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.reporting.presentation import generate_presentation_deck

if __name__ == "__main__":
    generate_presentation_deck()
