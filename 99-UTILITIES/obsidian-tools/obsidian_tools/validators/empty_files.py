"""Empty file validator for Obsidian vault.

Detects files with no content that should likely be removed.
"""

from pathlib import Path
from typing import List

from .base import ValidationResult, BaseValidator


class EmptyFileValidator(BaseValidator):
    """Validates that there are no empty files in the vault."""
    
    # Directories to exclude from empty file checking
    EXCLUDED_DIRS = {
        "external",
        "cross-validation/results",
        ".git",
        "__pycache__",
        "node_modules",
    }
    
    # Files that are allowed to be empty
    ALLOWED_EMPTY = {
        "__init__.py",  # Python package markers
        ".gitkeep",     # Git directory markers
    }
    
    def __init__(self, vault_path: Path):
        super().__init__(vault_path)
        self.empty_files: List[Path] = []
    
    @property
    def name(self) -> str:
        return "Empty Files"
    
    def _should_check_file(self, file_path: Path) -> bool:
        """Check if file should be included in empty file detection."""
        # Skip excluded directories
        for excluded in self.EXCLUDED_DIRS:
            if excluded in file_path.parts:
                return False
        
        # Skip allowed empty files
        if file_path.name in self.ALLOWED_EMPTY:
            return False
        
        # Only check markdown and python files
        if file_path.suffix not in {".md", ".py"}:
            return False
        
        return True
    
    def validate(self) -> ValidationResult:
        """Find empty files."""
        # Scan all files
        for file_path in self.vault_path.rglob("*"):
            if not file_path.is_file():
                continue
            
            if not self._should_check_file(file_path):
                continue
            
            # Check if file is empty
            try:
                if file_path.stat().st_size == 0:
                    self.empty_files.append(file_path)
                    self.add_warning(
                        file_path,
                        0,
                        "Empty file (consider removing or adding content)"
                    )
            except Exception:
                continue
        
        passed = len(self.issues) == 0
        
        return ValidationResult(
            validator_name=self.name,
            passed=passed,
            issues=self.issues,
            stats={
                "empty_files": len(self.empty_files)
            }
        )
