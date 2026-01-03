"""
Shared utilities for Obsidian vault operations.

License: CC0 1.0 Universal (Public Domain)
"""

import re
from pathlib import Path
from typing import List, Dict, Tuple, Optional


def find_markdown_files(vault_path: Path) -> List[Path]:
    """Find all markdown files in the vault."""
    return list(vault_path.rglob("*.md"))


def extract_wikilinks(content: str) -> List[Tuple[str, Optional[str]]]:
    """
    Extract wikilinks from markdown content.
    
    Returns:
        List of (target, heading) tuples. Heading is None if no heading link.
        
    Examples:
        [[note]] -> ("note", None)
        [[note#heading]] -> ("note", "heading")
    """
    pattern = r'\[\[([^\]#]+)(?:#([^\]]+))?\]\]'
    return [(m.group(1), m.group(2)) for m in re.finditer(pattern, content)]


def extract_markdown_links(content: str) -> List[str]:
    """
    Extract markdown-style links from content.
    
    Returns:
        List of link targets.
        
    Examples:
        [text](file.md) -> "file.md"
    """
    pattern = r'\[([^\]]+)\]\(([^\)]+)\)'
    return [m.group(2) for m in re.finditer(pattern, content)]


def extract_image_embeds(content: str) -> List[str]:
    """
    Extract image embeds from markdown content.
    
    Returns:
        List of image paths.
        
    Examples:
        ![[image.png]] -> "image.png"
    """
    pattern = r'!\[\[([^\]]+)\]\]'
    return [m.group(1) for m in re.finditer(pattern, content)]


def extract_frontmatter(content: str) -> Optional[Dict[str, str]]:
    """
    Extract YAML frontmatter from markdown content.
    
    Returns:
        Dict of frontmatter key-value pairs, or None if no frontmatter.
    """
    pattern = r'^---\n(.*?)\n---'
    match = re.match(pattern, content, re.DOTALL)
    
    if not match:
        return None
    
    frontmatter = {}
    yaml_content = match.group(1)
    
    for line in yaml_content.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            frontmatter[key.strip()] = value.strip()
    
    return frontmatter


def extract_headings(content: str) -> List[str]:
    """
    Extract all markdown headings from content.
    
    Returns:
        List of heading texts (without # markers).
    """
    pattern = r'^#+\s+(.+)$'
    return [m.group(1).strip() for m in re.finditer(pattern, content, re.MULTILINE)]


def normalize_path(path: str, base_path: Path) -> Path:
    """
    Normalize a wikilink path to a filesystem path.
    
    Handles:
    - Simple links: [[note]] -> note.md
    - Path links: [[folder/note]] -> folder/note.md
    - Already .md: [[note.md]] -> note.md
    """
    path = path.strip()
    
    # Add .md if not present
    if not path.endswith('.md'):
        path = f"{path}.md"
    
    # Convert to Path
    target = Path(path)
    
    # If absolute, return as-is
    if target.is_absolute():
        return target
    
    # Otherwise, resolve relative to base
    return (base_path / target).resolve()


def resolve_wikilink(link: str, vault_path: Path, current_file: Path) -> Optional[Path]:
    """
    Resolve a wikilink to an actual file path.
    
    Obsidian link resolution:
    1. Check relative to current file
    2. Search entire vault for matching filename
    
    Returns:
        Resolved Path or None if not found.
    """
    # Try relative to current file first
    current_dir = current_file.parent
    relative_target = normalize_path(link, current_dir)
    
    if relative_target.exists():
        return relative_target
    
    # Search entire vault for matching filename
    link_filename = link if link.endswith('.md') else f"{link}.md"
    
    for md_file in find_markdown_files(vault_path):
        if md_file.name == link_filename:
            return md_file
    
    return None
