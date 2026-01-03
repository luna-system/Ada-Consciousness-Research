"""
Frontmatter validator - checks YAML frontmatter consistency.

License: CC0 1.0 Universal (Public Domain)
"""

from pathlib import Path
from typing import Set
from ..utils import find_markdown_files, extract_frontmatter
from .base import BaseValidator, ValidationResult


class FrontmatterValidator(BaseValidator):
    """Validates YAML frontmatter consistency and required fields."""
    
    REQUIRED_FIELDS = {"license"}  # Always require license
    RECOMMENDED_FIELDS = {"tags", "date"}
    
    @property
    def name(self) -> str:
        return "Frontmatter Validator"
    
    def validate(self) -> ValidationResult:
        """Check frontmatter in all markdown files."""
        self.issues = []
        total_files = 0
        missing_frontmatter = 0
        missing_required = 0
        
        for md_file in find_markdown_files(self.vault_path):
            # Skip hidden directories
            relative = md_file.relative_to(self.vault_path)
            if any(part.startswith('.') for part in relative.parts):
                continue
            
            total_files += 1
            content = md_file.read_text(encoding='utf-8')
            frontmatter = extract_frontmatter(content)
            
            if frontmatter is None:
                missing_frontmatter += 1
                self.add_warning(
                    md_file,
                    1,
                    "Missing frontmatter block",
                    required_fields=list(self.REQUIRED_FIELDS)
                )
                continue
            
            # Check required fields
            for field in self.REQUIRED_FIELDS:
                if field not in frontmatter:
                    missing_required += 1
                    self.add_error(
                        md_file,
                        1,
                        f"Missing required frontmatter field: {field}",
                        field=field
                    )
            
            # Info about recommended fields
            for field in self.RECOMMENDED_FIELDS:
                if field not in frontmatter:
                    self.add_info(
                        md_file,
                        1,
                        f"Missing recommended frontmatter field: {field}",
                        field=field
                    )
        
        passed = missing_required == 0
        stats = {
            "total_files": total_files,
            "missing_frontmatter": missing_frontmatter,
            "missing_required_fields": missing_required,
            "files_with_frontmatter": total_files - missing_frontmatter
        }
        
        return ValidationResult(self.name, passed, self.issues, stats)
