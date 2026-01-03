"""
Link validator - checks for broken wikilinks and markdown links.

License: CC0 1.0 Universal (Public Domain)
"""

from pathlib import Path
from ..utils import find_markdown_files, extract_wikilinks, extract_markdown_links, resolve_wikilink
from .base import BaseValidator, ValidationResult


class LinkValidator(BaseValidator):
    """Validates that all wikilinks and markdown links point to existing files."""
    
    @property
    def name(self) -> str:
        return "Link Validator"
    
    def validate(self) -> ValidationResult:
        """Check all links in the vault."""
        self.issues = []
        total_links = 0
        broken_links = 0
        
        for md_file in find_markdown_files(self.vault_path):
            content = md_file.read_text(encoding='utf-8')
            lines = content.split('\n')
            
            # Check wikilinks
            for line_num, line in enumerate(lines, 1):
                wikilinks = extract_wikilinks(line)
                
                for link_target, heading in wikilinks:
                    total_links += 1
                    resolved = resolve_wikilink(link_target, self.vault_path, md_file)
                    
                    if resolved is None:
                        broken_links += 1
                        self.add_error(
                            md_file, 
                            line_num,
                            f"Broken wikilink: [[{link_target}]]",
                            link=link_target
                        )
                
                # Check markdown links (relative paths only)
                md_links = extract_markdown_links(line)
                for link in md_links:
                    if link.startswith(('http://', 'https://', '#')):
                        continue  # Skip external and anchor links
                    
                    total_links += 1
                    target_path = (md_file.parent / link).resolve()
                    
                    if not target_path.exists():
                        broken_links += 1
                        self.add_error(
                            md_file,
                            line_num,
                            f"Broken markdown link: [{link}]",
                            link=link
                        )
        
        passed = broken_links == 0
        stats = {
            "total_links": total_links,
            "broken_links": broken_links,
            "files_checked": len(list(find_markdown_files(self.vault_path)))
        }
        
        return ValidationResult(self.name, passed, self.issues, stats)
