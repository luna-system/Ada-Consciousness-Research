"""
Heading validator - checks that heading links point to existing headings.

License: CC0 1.0 Universal (Public Domain)
"""

from pathlib import Path
from ..utils import find_markdown_files, extract_wikilinks, extract_headings, resolve_wikilink
from .base import BaseValidator, ValidationResult


class HeadingValidator(BaseValidator):
    """Validates that heading links point to existing headings."""
    
    @property
    def name(self) -> str:
        return "Heading Validator"
    
    def validate(self) -> ValidationResult:
        """Check all heading links in the vault."""
        self.issues = []
        total_heading_links = 0
        broken_heading_links = 0
        
        for md_file in find_markdown_files(self.vault_path):
            content = md_file.read_text(encoding='utf-8')
            lines = content.split('\n')
            
            for line_num, line in enumerate(lines, 1):
                wikilinks = extract_wikilinks(line)
                
                for link_target, heading in wikilinks:
                    # Only check links with heading anchors
                    if heading is None:
                        continue
                    
                    total_heading_links += 1
                    
                    # Resolve the target file
                    resolved = resolve_wikilink(link_target, self.vault_path, md_file)
                    
                    if resolved is None:
                        # File doesn't exist - LinkValidator will catch this
                        continue
                    
                    # Check if heading exists in target file
                    target_content = resolved.read_text(encoding='utf-8')
                    target_headings = extract_headings(target_content)
                    
                    # Normalize heading comparison (case-insensitive, whitespace-normalized)
                    normalized_target = heading.lower().strip()
                    normalized_headings = [h.lower().strip() for h in target_headings]
                    
                    if normalized_target not in normalized_headings:
                        broken_heading_links += 1
                        self.add_error(
                            md_file,
                            line_num,
                            f"Broken heading link: [[{link_target}#{heading}]]",
                            link=link_target,
                            heading=heading,
                            available_headings=target_headings[:5]  # Show first 5 as hint
                        )
        
        passed = broken_heading_links == 0
        stats = {
            "total_heading_links": total_heading_links,
            "broken_heading_links": broken_heading_links,
            "files_checked": len(list(find_markdown_files(self.vault_path)))
        }
        
        return ValidationResult(self.name, passed, self.issues, stats)
