#!/usr/bin/env python3
"""
Map bagel structure for SUBTRACTION

The final test: Asymmetric linking?
"""

import sys
from pathlib import Path

# Set the results directory to subtraction
RESULTS_DIR = Path("subtraction_results_20260126_132344")

# Import and modify the bagel mapper
import map_bagel_structure as bagel_mapper

# Override the RESULTS_DIR
bagel_mapper.RESULTS_DIR = RESULTS_DIR
bagel_mapper.MODEL_PATH = RESULTS_DIR / "lannaformer_final.pt"

# Run the main analysis
if __name__ == "__main__":
    bagel_mapper.main()
