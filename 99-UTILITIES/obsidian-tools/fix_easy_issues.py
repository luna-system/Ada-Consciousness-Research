#!/usr/bin/env python3
"""
Quick fixes for common vault issues
====================================

Fixes:
1. Folder renames (10-SPECIFICATIONS → 01-FOUNDATIONS, 05-FINDINGS → 07-ANALYSES/findings)
2. Add frontmatter to top-level docs

License: CC0 1.0 Universal (Public Domain)
"""

import re
from pathlib import Path
from datetime import datetime


def fix_folder_references(vault_path: Path) -> int:
    """Fix outdated folder references in markdown files."""
    fixes = 0
    
    replacements = [
        (r'\[10-SPECIFICATIONS/', '[01-FOUNDATIONS/'),
        (r'\[\[10-SPECIFICATIONS/', '[[01-FOUNDATIONS/'),
        (r'10-SPECIFICATIONS/', '01-FOUNDATIONS/'),
        (r'\[05-FINDINGS/', '[07-ANALYSES/findings/'),
        (r'\[\[05-FINDINGS/', '[[07-ANALYSES/findings/'),
    ]
    
    for md_file in vault_path.rglob("*.md"):
        content = md_file.read_text(encoding='utf-8')
        original_content = content
        
        for pattern, replacement in replacements:
            content = re.sub(pattern, replacement, content)
        
        if content != original_content:
            md_file.write_text(content, encoding='utf-8')
            fixes += 1
            print(f"  ✓ Fixed: {md_file.relative_to(vault_path)}")
    
    return fixes


def add_frontmatter(file_path: Path, license_type: str = "CC-BY-4.0") -> bool:
    """Add frontmatter to a file if missing."""
    content = file_path.read_text(encoding='utf-8')
    
    # Skip if already has frontmatter
    if content.startswith('---'):
        return False
    
    # Determine title from filename
    title = file_path.stem.replace('-', ' ').replace('_', ' ')
    
    # Create frontmatter
    frontmatter = f"""---
license: {license_type}
date: {datetime.now().strftime('%Y-%m-%d')}
tags: [documentation]
---

"""
    
    # Add frontmatter
    new_content = frontmatter + content
    file_path.write_text(new_content, encoding='utf-8')
    
    return True


def fix_top_level_frontmatter(vault_path: Path) -> int:
    """Add frontmatter to key top-level documentation files."""
    fixes = 0
    
    # Research docs get CC-BY
    research_files = [
        "00-DASHBOARD.md",
        "README.md",
        "QUICK-START-GUIDE.md",
        "EXPERIMENT-REGISTRY.md",
        "FINDINGS-CROSS-REFERENCE-MAP.md",
    ]
    
    for filename in research_files:
        file_path = vault_path / filename
        if file_path.exists():
            if add_frontmatter(file_path, "CC-BY-4.0"):
                fixes += 1
                print(f"  ✓ Added frontmatter: {filename}")
    
    return fixes


def main():
    vault_path = Path(__file__).parent.parent.parent
    
    print("=" * 70)
    print("EASY FIXES FOR OBSIDIAN VAULT")
    print("=" * 70)
    print()
    
    print("1. Fixing folder references...")
    folder_fixes = fix_folder_references(vault_path)
    print(f"   → Fixed {folder_fixes} files\n")
    
    print("2. Adding frontmatter to top-level docs...")
    frontmatter_fixes = fix_top_level_frontmatter(vault_path)
    print(f"   → Added frontmatter to {frontmatter_fixes} files\n")
    
    print("=" * 70)
    print(f"TOTAL: {folder_fixes + frontmatter_fixes} fixes applied")
    print("=" * 70)
    print()
    print("Bigger fixes to plan:")
    print("  - Add frontmatter to all research docs (466 files)")
    print("  - Fix remaining wikilinks to missing files")
    print("  - Review orphaned files (383 files)")
    print()


if __name__ == "__main__":
    main()
