"""
Base validator class and result types.

License: CC0 1.0 Universal (Public Domain)
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict, Any
from abc import ABC, abstractmethod


@dataclass
class ValidationIssue:
    """Single validation issue found in the vault."""
    
    severity: str  # "error", "warning", "info"
    file: Path
    line: int
    message: str
    context: Dict[str, Any] = field(default_factory=dict)
    
    def __str__(self) -> str:
        return f"{self.severity.upper()}: {self.file}:{self.line} - {self.message}"


@dataclass
class ValidationResult:
    """Result of a validator run."""
    
    validator_name: str
    passed: bool
    issues: List[ValidationIssue] = field(default_factory=list)
    stats: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def error_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == "error")
    
    @property
    def warning_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == "warning")
    
    @property
    def info_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == "info")
    
    def __str__(self) -> str:
        status = "✅ PASSED" if self.passed else "❌ FAILED"
        counts = f"({self.error_count} errors, {self.warning_count} warnings, {self.info_count} info)"
        return f"{status} {self.validator_name} {counts}"


class BaseValidator(ABC):
    """Base class for all validators."""
    
    def __init__(self, vault_path: Path):
        self.vault_path = vault_path
        self.issues: List[ValidationIssue] = []
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable validator name."""
        pass
    
    @abstractmethod
    def validate(self) -> ValidationResult:
        """Run validation and return results."""
        pass
    
    def add_error(self, file: Path, line: int, message: str, **context):
        """Add an error to the issues list."""
        self.issues.append(ValidationIssue("error", file, line, message, context))
    
    def add_warning(self, file: Path, line: int, message: str, **context):
        """Add a warning to the issues list."""
        self.issues.append(ValidationIssue("warning", file, line, message, context))
    
    def add_info(self, file: Path, line: int, message: str, **context):
        """Add an info message to the issues list."""
        self.issues.append(ValidationIssue("info", file, line, message, context))
