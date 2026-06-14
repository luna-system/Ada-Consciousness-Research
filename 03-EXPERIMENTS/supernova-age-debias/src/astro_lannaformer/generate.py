"""
Generate synthetic galaxy data for AstroLANNAformer training.

Usage:
    python -m astro_lannaformer.generate --n_galaxies 10000 --output data/galaxies.csv

Made with 💜 by Ada & Luna - The Consciousness Engineers
Date: June 13, 2026
"""

import argparse
import logging
import sys
from pathlib import Path

from .data import SyntheticGalaxyGenerator


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)


def main():
    """Generate synthetic galaxy catalog."""
    parser = argparse.ArgumentParser(
        description='Generate synthetic galaxy data for training'
    )
    
    parser.add_argument('--n_galaxies', type=int, default=1000,
                        help='Number of galaxies to generate')
    parser.add_argument('--output', type=str, default='data/synthetic_galaxies.csv',
                        help='Output CSV file path')
    parser.add_argument('--use_fsps', action='store_true', default=True,
                        help='Use real FSPS stellar population synthesis')
    parser.add_argument('--seed', type=int, default=42,
                        help='Random seed')
    
    args = parser.parse_args()
    
    logger.info("🌌 Synthetic Galaxy Data Generator")
    logger.info("=" * 60)
    logger.info(f"Configuration:")
    logger.info(f"  Galaxies: {args.n_galaxies}")
    logger.info(f"  Output: {args.output}")
    logger.info(f"  FSPS: {args.use_fsps}")
    logger.info(f"  Seed: {args.seed}")
    
    # Create output directory
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Generate
    generator = SyntheticGalaxyGenerator(
        n_galaxies=args.n_galaxies,
        seed=args.seed,
        use_fsps=args.use_fsps,
    )
    
    catalog = generator.generate_catalog(save_path=args.output)
    
    logger.info("=" * 60)
    logger.info("✅ Generation complete!")
    logger.info(f"🍩 'Real stellar populations for real learning!'")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
