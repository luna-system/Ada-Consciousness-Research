"""
Image validator - checks for broken image embeds.

License: CC0 1.0 Universal (Public Domain)
"""

from pathlib import Path
from ..utils import find_markdown_files, extract_image_embeds
from .base import BaseValidator, ValidationResult


class ImageValidator(BaseValidator):
    """Validates that all image embeds point to existing files."""
    
    @property
    def name(self) -> str:
        return "Image Validator"
    
    def validate(self) -> ValidationResult:
        """Check all image embeds in the vault."""
        self.issues = []
        total_images = 0
        broken_images = 0
        
        for md_file in find_markdown_files(self.vault_path):
            content = md_file.read_text(encoding='utf-8')
            lines = content.split('\n')
            
            for line_num, line in enumerate(lines, 1):
                images = extract_image_embeds(line)
                
                for image_path in images:
                    total_images += 1
                    
                    # Check relative to file location first
                    target = (md_file.parent / image_path).resolve()
                    
                    # Also check common attachment folders
                    if not target.exists():
                        alt_paths = [
                            self.vault_path / "attachments" / image_path,
                            self.vault_path / "assets" / image_path,
                            self.vault_path / image_path,
                        ]
                        
                        found = any(p.exists() for p in alt_paths)
                        
                        if not found:
                            broken_images += 1
                            self.add_error(
                                md_file,
                                line_num,
                                f"Broken image embed: ![[{image_path}]]",
                                image_path=image_path
                            )
        
        passed = broken_images == 0
        stats = {
            "total_images": total_images,
            "broken_images": broken_images,
            "files_checked": len(list(find_markdown_files(self.vault_path)))
        }
        
        return ValidationResult(self.name, passed, self.issues, stats)
