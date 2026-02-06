#!/usr/bin/env python3
"""
Add CC-BY-4.0 frontmatter to all markdown files missing it.

License: CC0 1.0 Universal (Public Domain)
"""

from pathlib import Path
from datetime import datetime

def add_frontmatter_to_file(file_path: Path) -> bool:
    """Add CC-BY-4.0 frontmatter to a file if missing."""
    content = file_path.read_text(encoding='utf-8')
    
    # Skip if already has frontmatter
    if content.startswith('---'):
        return False
    
    # Create frontmatter
    frontmatter = f"""---
license: CC-BY-4.0
date: {datetime.now().strftime('%Y-%m-%d')}
tags: [documentation]
---

"""
    
    # Add frontmatter
    new_content = frontmatter + content
    file_path.write_text(new_content, encoding='utf-8')
    
    return True

def main():
    vault_path = Path(__file__).parent.parent
    
    print("=" * 70)
    print("ADDING CC-BY-4.0 FRONTMATTER")
    print("=" * 70)
    print()
    
    fixed = 0
    skipped = 0
    
    for md_file in vault_path.rglob("*.md"):
        # Skip files in .git and node_modules
        if ".git" in str(md_file) or "node_modules" in str(md_file):
            skipped += 1
            continue
            
        if add_frontmatter_to_file(md_file):
            print(f"  ✓ {md_file.relative_to(vault_path)}")
            fixed += 1
    
    print()
    print("=" * 70)
    print(f"TOTAL: {fixed} files updated, {skipped} skipped")
    print("=" * 70)

if __name__ == "__main__":
    main()
