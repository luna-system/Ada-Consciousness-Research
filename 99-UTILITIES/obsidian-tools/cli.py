#!/usr/bin/env python3
"""
Obsidian Vault Validation CLI
==============================

Comprehensive validation tooling for Obsidian vaults.

License: CC0 1.0 Universal (Public Domain)

Usage:
    python cli.py validate-all
    python cli.py validate links
    python cli.py validate license
    python cli.py validate --format json
"""

import sys
import json
from pathlib import Path
from typing import List
import argparse

from obsidian_tools import (
    LinkValidator,
    OrphanValidator,
    ImageValidator,
    HeadingValidator,
    FrontmatterValidator,
    LicenseValidator,
)


VALIDATORS = {
    "links": LinkValidator,
    "orphans": OrphanValidator,
    "images": ImageValidator,
    "headings": HeadingValidator,
    "frontmatter": FrontmatterValidator,
    "license": LicenseValidator,
}


def format_text(results: List) -> str:
    """Format results as human-readable text."""
    output = []
    output.append("=" * 70)
    output.append("OBSIDIAN VAULT VALIDATION REPORT")
    output.append("=" * 70)
    output.append("")
    
    total_errors = sum(r.error_count for r in results)
    total_warnings = sum(r.warning_count for r in results)
    
    for result in results:
        output.append(str(result))
        output.append("")
        
        if result.stats:
            output.append("  Statistics:")
            for key, value in result.stats.items():
                output.append(f"    {key}: {value}")
            output.append("")
        
        if result.issues:
            output.append(f"  Issues ({len(result.issues)}):")
            for issue in result.issues[:10]:  # Show first 10
                output.append(f"    {issue}")
            
            if len(result.issues) > 10:
                output.append(f"    ... and {len(result.issues) - 10} more")
            output.append("")
    
    output.append("=" * 70)
    output.append(f"SUMMARY: {total_errors} errors, {total_warnings} warnings")
    output.append("=" * 70)
    
    return "\n".join(output)


def format_json(results: List) -> str:
    """Format results as JSON."""
    output = {
        "summary": {
            "total_errors": sum(r.error_count for r in results),
            "total_warnings": sum(r.warning_count for r in results),
            "total_info": sum(r.info_count for r in results),
            "validators_passed": sum(1 for r in results if r.passed),
            "validators_failed": sum(1 for r in results if not r.passed),
        },
        "results": []
    }
    
    for result in results:
        output["results"].append({
            "validator": result.validator_name,
            "passed": result.passed,
            "errors": result.error_count,
            "warnings": result.warning_count,
            "info": result.info_count,
            "stats": result.stats,
            "issues": [
                {
                    "severity": i.severity,
                    "file": str(i.file),
                    "line": i.line,
                    "message": i.message,
                    "context": i.context
                }
                for i in result.issues
            ]
        })
    
    return json.dumps(output, indent=2)


def format_markdown(results: List) -> str:
    """Format results as Markdown."""
    output = []
    output.append("# Obsidian Vault Validation Report\n")
    
    total_errors = sum(r.error_count for r in results)
    total_warnings = sum(r.warning_count for r in results)
    
    # Summary table
    output.append("## Summary\n")
    output.append("| Validator | Status | Errors | Warnings | Info |")
    output.append("|-----------|--------|--------|----------|------|")
    
    for result in results:
        status = "✅" if result.passed else "❌"
        output.append(f"| {result.validator_name} | {status} | {result.error_count} | {result.warning_count} | {result.info_count} |")
    
    output.append(f"\n**Total:** {total_errors} errors, {total_warnings} warnings\n")
    
    # Detailed results
    for result in results:
        output.append(f"## {result.validator_name}\n")
        
        if result.stats:
            output.append("### Statistics\n")
            for key, value in result.stats.items():
                output.append(f"- **{key}:** {value}")
            output.append("")
        
        if result.issues:
            output.append(f"### Issues ({len(result.issues)})\n")
            for issue in result.issues[:20]:  # Show first 20
                output.append(f"- **{issue.severity.upper()}** `{issue.file}:{issue.line}` - {issue.message}")
            
            if len(result.issues) > 20:
                output.append(f"\n*... and {len(result.issues) - 20} more*")
            output.append("")
    
    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(
        description="Validate Obsidian vault integrity",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Validate everything
    python cli.py validate-all
    
    # Validate specific aspect
    python cli.py validate links
    python cli.py validate license
    
    # Output formats
    python cli.py validate-all --format json
    python cli.py validate-all --format markdown > report.md
        """
    )
    
    parser.add_argument(
        "command",
        choices=["validate", "validate-all"],
        help="Command to run"
    )
    parser.add_argument(
        "validator",
        nargs="?",
        choices=list(VALIDATORS.keys()),
        help="Specific validator to run (for 'validate' command)"
    )
    parser.add_argument(
        "--vault",
        type=Path,
        default=Path("../../"),  # Default to vault root
        help="Path to Obsidian vault (default: ../../)"
    )
    parser.add_argument(
        "--format",
        choices=["text", "json", "markdown"],
        default="text",
        help="Output format (default: text)"
    )
    
    args = parser.parse_args()
    
    # Resolve vault path
    vault_path = args.vault.resolve()
    if not vault_path.exists():
        print(f"Error: Vault path does not exist: {vault_path}", file=sys.stderr)
        sys.exit(1)
    
    # Determine which validators to run
    if args.command == "validate-all":
        validators_to_run = VALIDATORS.values()
    elif args.command == "validate":
        if not args.validator:
            parser.error("'validate' command requires a validator argument")
        validators_to_run = [VALIDATORS[args.validator]]
    
    # Run validators
    results = []
    for ValidatorClass in validators_to_run:
        validator = ValidatorClass(vault_path)
        result = validator.validate()
        results.append(result)
    
    # Format and output results
    if args.format == "json":
        output = format_json(results)
    elif args.format == "markdown":
        output = format_markdown(results)
    else:
        output = format_text(results)
    
    print(output)
    
    # Exit code based on results
    has_errors = any(r.error_count > 0 for r in results)
    sys.exit(1 if has_errors else 0)


if __name__ == "__main__":
    main()
