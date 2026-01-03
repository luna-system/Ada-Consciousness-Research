"""
Orphan validator - finds files with no incoming links.

License: CC0 1.0 Universal (Public Domain)
"""

from pathlib import Path
from collections import defaultdict
from ..utils import find_markdown_files, extract_wikilinks, resolve_wikilink
from .base import BaseValidator, ValidationResult


class OrphanValidator(BaseValidator):
    """Finds markdown files that have no incoming links (orphans)."""
    
    @property
    def name(self) -> str:
        return "Orphan Validator"
    
    def validate(self) -> ValidationResult:
        """Find all orphaned files in the vault."""
        self.issues = []
        
        # Build a map of all files and their incoming links
        all_files = set(find_markdown_files(self.vault_path))
        incoming_links = defaultdict(set)
        
        # Scan all files for links
        for md_file in all_files:
            content = md_file.read_text(encoding='utf-8')
            wikilinks = extract_wikilinks(content)
            
            for link_target, _ in wikilinks:
                resolved = resolve_wikilink(link_target, self.vault_path, md_file)
                if resolved:
                    incoming_links[resolved].add(md_file)
        
        # Find orphans (files with no incoming links)
        orphans = []
        for file_path in all_files:
            # Skip index files and certain directories
            if file_path.name in ['README.md', 'index.md', 'INDEX.md']:
                continue
            
            if file_path not in incoming_links:
                orphans.append(file_path)
                self.add_info(
                    file_path,
                    0,
                    "Orphaned file (no incoming links)",
                    relative_path=str(file_path.relative_to(self.vault_path))
                )
        
        # Orphans are info, not errors
        passed = True
        stats = {
            "total_files": len(all_files),
            "orphaned_files": len(orphans),
            "connected_files": len(all_files) - len(orphans)
        }
        
        return ValidationResult(self.name, passed, self.issues, stats)
