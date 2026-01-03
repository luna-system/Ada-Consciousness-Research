"""
Obsidian Vault Tools
====================

Modular validation and analysis tools for Obsidian vaults.

License: CC0 1.0 Universal (Public Domain)
"""

from .validators.links import LinkValidator
from .validators.orphans import OrphanValidator
from .validators.images import ImageValidator
from .validators.headings import HeadingValidator
from .validators.frontmatter import FrontmatterValidator
from .validators.license import LicenseValidator

__all__ = [
    "LinkValidator",
    "OrphanValidator", 
    "ImageValidator",
    "HeadingValidator",
    "FrontmatterValidator",
    "LicenseValidator",
]

__version__ = "0.1.0"
