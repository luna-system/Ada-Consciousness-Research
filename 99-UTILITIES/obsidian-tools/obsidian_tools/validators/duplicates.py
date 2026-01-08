"""Duplicate file validator for Obsidian vault.

Detects duplicate files by content hash, excluding expected duplicates
from external repositories.
"""

import hashlib
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Set

from .base import ValidationResult, BaseValidator


class DuplicateValidator(BaseValidator):
    """Validates that there are no unexpected duplicate files in the vault."""
    
    @property
    def name(self) -> str:
        return "Duplicate Files"
    
    # Directories to exclude from duplicate checking (external repos)
    EXCLUDED_DIRS = {
        "external",
        "cross-validation/results",
        ".git",
        "__pycache__",
        "node_modules",
    }
    
    def __init__(self, vault_path: Path):
        super().__init__(vault_path)
        self.duplicates: Dict[str, List[Path]] = defaultdict(list)
        self.empty_files: List[Path] = []
    
    def _should_check_file(self, file_path: Path) -> bool:
        """Check if file should be included in duplicate detection."""
        # Skip excluded directories
        for excluded in self.EXCLUDED_DIRS:
            if excluded in file_path.parts:
                return False
        
        # Only check markdown and python files
        if file_path.suffix not in {".md", ".py"}:
            return False
        
        return True
    
    def _compute_hash(self, file_path: Path) -> str:
        """Compute MD5 hash of file content."""
        try:
            with open(file_path, "rb") as f:
                return hashlib.md5(f.read()).hexdigest()
        except Exception:
            return ""
    
    def validate(self) -> ValidationResult:
        """Find duplicate files by content hash."""
        hash_to_files: Dict[str, List[Path]] = defaultdict(list)
        
        # Scan all files
        for file_path in self.vault_path.rglob("*"):
            if not file_path.is_file():
                continue
            
            if not self._should_check_file(file_path):
                continue
            
            file_hash = self._compute_hash(file_path)
            if not file_hash:
                continue
            
            # Check for empty files
            if file_hash == "d41d8cd98f00b204e9800998ecf8427e":  # MD5 of empty file
                self.empty_files.append(file_path)
            
            hash_to_files[file_hash].append(file_path)
        
        # Find duplicates (files with same hash)
        for file_hash, files in hash_to_files.items():
            if len(files) > 1:
                # Convert to relative paths for readability
                rel_paths = [f.relative_to(self.vault_path) for f in files]
                self.duplicates[file_hash] = rel_paths
        
        # Add issues for empty files
        for empty_file in self.empty_files:
            self.add_warning(
                empty_file,
                0,
                "Empty file (consider removing)"
            )
        
        # Add issues for duplicates
        for file_hash, files in self.duplicates.items():
            # Report on first file, mention duplicates
            if files:
                duplicates_str = ", ".join(str(f) for f in files[1:])
                self.add_warning(
                    self.vault_path / files[0],
                    0,
                    f"Duplicate content found in: {duplicates_str}"
                )
        
        passed = len(self.issues) == 0
        
        return ValidationResult(
            validator_name=self.name,
            passed=passed,
            issues=self.issues,
            stats={
                "empty_files": len(self.empty_files),
                "duplicate_sets": len(self.duplicates),
                "total_duplicates": sum(len(files) for files in self.duplicates.values())
            }
        )
