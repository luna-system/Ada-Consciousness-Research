---
license: CC-BY-4.0
date: 2026-02-06
tags: [documentation]
---

# Obsidian Vault Validation Tools

Modular, extensible validation and analysis tooling for Obsidian vaults.

## Features

### Validators

- **LinkValidator** - Finds broken wikilinks and markdown links
- **OrphanValidator** - Identifies files with no incoming links
- **ImageValidator** - Checks for broken image embeds
- **HeadingValidator** - Validates heading anchor links
- **FrontmatterValidator** - Ensures consistent YAML frontmatter
- **LicenseValidator** - Enforces licensing policy (CC0 for code, CC-BY for research)

### Output Formats

- **Text** - Human-readable terminal output
- **JSON** - Machine-parsable for CI/CD
- **Markdown** - Report generation

## Usage

### Basic Validation

```bash
# Validate everything
python cli.py validate-all

# Validate specific aspect
python cli.py validate links
python cli.py validate license
python cli.py validate orphans
```

### Output Formats

```bash
# JSON output (for CI/CD)
python cli.py validate-all --format json

# Markdown report
python cli.py validate-all --format markdown > report.md
```

### Custom Vault Path

```bash
python cli.py validate-all --vault /path/to/vault
```

## License Policy

The LicenseValidator enforces:

- **Code/Utilities** (`99-UTILITIES/`, `scripts/`) → **CC0** (Public Domain)
- **Research** (`00-INDEX/`, `01-THEORY/`, `02-SPECS/`, `03-EXPERIMENTS/`) → **CC-BY 4.0**
- **Model-specific** → Respects model licenses (Apache 2.0, MIT, etc.)

## Architecture

### Modular Design

```
obsidian_tools/
├── validators/
│   ├── base.py          # BaseValidator + ValidationResult
│   ├── links.py         # LinkValidator
│   ├── orphans.py       # OrphanValidator
│   ├── images.py        # ImageValidator
│   ├── headings.py      # HeadingValidator
│   ├── frontmatter.py   # FrontmatterValidator
│   └── license.py       # LicenseValidator
└── utils.py             # Shared utilities
```

### Extending

Create a new validator by inheriting from `BaseValidator`:

```python
from obsidian_tools.validators.base import BaseValidator, ValidationResult

class MyValidator(BaseValidator):
    @property
    def name(self) -> str:
        return "My Custom Validator"
    
    def validate(self) -> ValidationResult:
        # Your validation logic
        self.add_error(file_path, line_num, "Error message")
        return ValidationResult(self.name, passed, self.issues, stats)
```

## CI/CD Integration

### GitHub Actions Example

```yaml
- name: Validate Vault
  run: |
    cd 99-UTILITIES/obsidian-tools
    python cli.py validate-all --format json > report.json
    
- name: Upload Report
  uses: actions/upload-artifact@v3
  with:
    name: validation-report
    path: report.json
```

### Exit Codes

- `0` - All validators passed
- `1` - One or more validators found errors

## License

CC0 1.0 Universal (Public Domain)

This tool is dedicated to the public domain. You can copy, modify, distribute and perform the work, even for commercial purposes, all without asking permission.

---

**Built with 💜 by Luna + Ada**  
*Part of the Ada Consciousness Research Project*
