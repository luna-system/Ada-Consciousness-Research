#!/usr/bin/env python3
"""
Map bagel structure for MULTIPLICATION

Quick test: Do we get the same 5 bagels?
"""

import sys
from pathlib import Path

# Set the results directory to multiplication
RESULTS_DIR = Path("multiplication_results_20260126_125047")

# Import and modify the bagel mapper
import map_bagel_structure as bagel_mapper

# Override the RESULTS_DIR
bagel_mapper.RESULTS_DIR = RESULTS_DIR
bagel_mapper.MODEL_PATH = RESULTS_DIR / "lannaformer_final.pt"

# Run the main analysis
if __name__ == "__main__":
    bagel_mapper.main()
