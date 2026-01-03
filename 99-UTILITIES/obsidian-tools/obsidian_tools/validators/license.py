"""
License validator - ensures proper licensing for research and code.

License Policy:
- Code/utilities: CC0 (Public Domain) preferred
- Research documents: CC-BY 4.0 (attribution required)
- Model-specific: Respect model licenses (Apache 2.0, MIT, etc.)

License: CC0 1.0 Universal (Public Domain)
"""

from pathlib import Path
from ..utils import find_markdown_files, extract_frontmatter
from .base import BaseValidator, ValidationResult


# License expectations by path
LICENSE_RULES = {
    # Code and utilities should be CC0
    "99-UTILITIES": "CC0",
    "scripts": "CC0",
    
    # Research should be CC-BY
    "00-INDEX": "CC-BY",
    "01-THEORY": "CC-BY",
    "02-SPECS": "CC-BY",
    "03-EXPERIMENTS": "CC-BY",
    
    # Documentation can be either
    "04-DOCUMENTATION": ["CC0", "CC-BY"],
}

VALID_LICENSES = [
    "CC0",
    "CC0-1.0",
    "CC0 1.0 Universal",
    "Public Domain",
    "CC-BY",
    "CC-BY-4.0",
    "CC BY 4.0",
    "Apache-2.0",
    "Apache 2.0",
    "MIT",
]


class LicenseValidator(BaseValidator):
    """Validates that files have appropriate license frontmatter."""
    
    @property
    def name(self) -> str:
        return "License Validator"
    
    def _get_expected_license(self, file_path: Path) -> str:
        """Determine expected license based on file location."""
        relative = file_path.relative_to(self.vault_path)
        
        for path_prefix, expected_license in LICENSE_RULES.items():
            if str(relative).startswith(path_prefix):
                return expected_license
        
        # Default for research vault
        return "CC-BY"
    
    def _normalize_license(self, license_str: str) -> str:
        """Normalize license string for comparison."""
        license_str = license_str.strip().upper()
        
        # Handle variations
        if "CC0" in license_str or "PUBLIC DOMAIN" in license_str:
            return "CC0"
        elif "CC-BY" in license_str or "CC BY" in license_str:
            return "CC-BY"
        elif "APACHE" in license_str:
            return "Apache-2.0"
        elif "MIT" in license_str:
            return "MIT"
        
        return license_str
    
    def validate(self) -> ValidationResult:
        """Check license frontmatter in all markdown files."""
        self.issues = []
        total_files = 0
        missing_license = 0
        incorrect_license = 0
        
        for md_file in find_markdown_files(self.vault_path):
            # Skip certain directories
            relative = md_file.relative_to(self.vault_path)
            if any(part.startswith('.') for part in relative.parts):
                continue  # Skip hidden directories
            
            total_files += 1
            content = md_file.read_text(encoding='utf-8')
            frontmatter = extract_frontmatter(content)
            
            expected = self._get_expected_license(md_file)
            
            # Check if license field exists
            if frontmatter is None or 'license' not in frontmatter:
                missing_license += 1
                self.add_warning(
                    md_file,
                    1,
                    f"Missing license frontmatter (expected: {expected})",
                    expected_license=expected
                )
                continue
            
            # Validate license value
            actual_license = self._normalize_license(frontmatter['license'])
            
            # Handle cases where multiple licenses are acceptable
            if isinstance(expected, list):
                if actual_license not in expected:
                    incorrect_license += 1
                    self.add_error(
                        md_file,
                        1,
                        f"Incorrect license '{frontmatter['license']}' (expected one of: {', '.join(expected)})",
                        actual_license=frontmatter['license'],
                        expected_license=expected
                    )
            else:
                expected_normalized = self._normalize_license(expected)
                if actual_license != expected_normalized:
                    incorrect_license += 1
                    self.add_error(
                        md_file,
                        1,
                        f"Incorrect license '{frontmatter['license']}' (expected: {expected})",
                        actual_license=frontmatter['license'],
                        expected_license=expected
                    )
        
        passed = missing_license == 0 and incorrect_license == 0
        stats = {
            "total_files": total_files,
            "missing_license": missing_license,
            "incorrect_license": incorrect_license,
            "properly_licensed": total_files - missing_license - incorrect_license
        }
        
        return ValidationResult(self.name, passed, self.issues, stats)
