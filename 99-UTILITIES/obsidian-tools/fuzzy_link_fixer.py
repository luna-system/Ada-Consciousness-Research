#!/usr/bin/env python3
"""
Fuzzy Link Fixer for Obsidian Vault
====================================

Uses fuzzy matching to find and fix broken links automatically.

Strategy:
1. Cache all .md files in vault (path + filename)
2. For each broken link, fuzzy match against cache
3. Suggest best matches with confidence scores
4. Auto-fix high-confidence matches (>90%)
5. Show medium-confidence for review (70-90%)

License: CC0 1.0 Universal (Public Domain)
"""

import re
from pathlib import Path
from difflib import SequenceMatcher
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass
from collections import defaultdict


@dataclass
class LinkMatch:
    """A potential match for a broken link."""
    broken_link: str
    file_path: Path
    confidence: float
    link_type: str  # 'wikilink' or 'markdown'
    
    def __str__(self) -> str:
        return f"{self.confidence:.1%} - {self.file_path}"


class FuzzyLinkFixer:
    """Fuzzy matcher for broken Obsidian links."""
    
    def __init__(self, vault_path: Path):
        self.vault_path = vault_path
        self.file_cache: Dict[str, List[Path]] = defaultdict(list)
        self._build_cache()
    
    def _build_cache(self) -> None:
        """Build cache of all markdown files."""
        print("📦 Building file cache...")
        for md_file in self.vault_path.rglob("*.md"):
            # Cache by filename (for exact matches)
            filename = md_file.name
            self.file_cache[filename].append(md_file)
            
            # Cache by stem (without .md)
            stem = md_file.stem
            self.file_cache[stem].append(md_file)
        
        print(f"   → Cached {len(list(self.vault_path.rglob('*.md')))} files")
    
    def _similarity(self, a: str, b: str) -> float:
        """Calculate similarity between two strings (0.0 to 1.0)."""
        return SequenceMatcher(None, a.lower(), b.lower()).ratio()
    
    def _extract_filename(self, link: str) -> str:
        """Extract filename from a link path."""
        # Handle markdown links: [text](path/file.md)
        if '/' in link:
            link = link.split('/')[-1]
        
        # Remove .md extension
        if link.endswith('.md'):
            link = link[:-3]
        
        # Remove heading anchors
        if '#' in link:
            link = link.split('#')[0]
        
        return link.strip()
    
    def find_matches(self, broken_link: str, link_type: str = 'wikilink') -> List[LinkMatch]:
        """Find potential matches for a broken link."""
        filename = self._extract_filename(broken_link)
        
        # First try exact match
        exact_matches = self.file_cache.get(filename, [])
        if exact_matches:
            return [LinkMatch(broken_link, path, 1.0, link_type) for path in exact_matches]
        
        # Fuzzy match against all files
        matches = []
        for md_file in self.vault_path.rglob("*.md"):
            stem = md_file.stem
            
            # Calculate similarity
            sim = self._similarity(filename, stem)
            
            if sim >= 0.7:  # Only consider 70%+ matches
                matches.append(LinkMatch(broken_link, md_file, sim, link_type))
        
        # Sort by confidence (highest first)
        matches.sort(key=lambda m: m.confidence, reverse=True)
        
        # Return top 5 matches
        return matches[:5]
    
    def fix_broken_links_in_file(self, file_path: Path, dry_run: bool = True) -> Dict:
        """Find and fix broken links in a specific file."""
        content = file_path.read_text(encoding='utf-8')
        original_content = content
        
        stats = {
            'file': file_path,
            'fixes': [],
            'needs_review': [],
            'no_match': []
        }
        
        # Find wikilinks [[...]]
        for match in re.finditer(r'\[\[([^\]]+)\]\]', content):
            link_text = match.group(1)
            
            # Check if file exists
            potential_path = self.vault_path / f"{link_text}.md"
            if potential_path.exists():
                continue  # Link is valid
            
            # Try to find matches
            matches = self.find_matches(link_text, 'wikilink')
            
            if not matches:
                stats['no_match'].append(link_text)
            elif matches[0].confidence >= 0.9:
                # High confidence - auto-fix
                best = matches[0]
                new_link = best.file_path.stem
                content = content.replace(f"[[{link_text}]]", f"[[{new_link}]]")
                stats['fixes'].append({
                    'old': link_text,
                    'new': new_link,
                    'confidence': best.confidence
                })
            else:
                # Medium confidence - needs review
                stats['needs_review'].append({
                    'link': link_text,
                    'matches': matches
                })
        
        # Find markdown links [text](path)
        for match in re.finditer(r'\[([^\]]+)\]\(([^\)]+)\)', content):
            link_text = match.group(1)
            link_path = match.group(2)
            
            # Skip external links
            if link_path.startswith('http'):
                continue
            
            # Check if file exists
            potential_path = self.vault_path / link_path
            if potential_path.exists():
                continue  # Link is valid
            
            # Try to find matches
            matches = self.find_matches(link_path, 'markdown')
            
            if not matches:
                stats['no_match'].append(link_path)
            elif matches[0].confidence >= 0.9:
                # High confidence - auto-fix
                best = matches[0]
                new_path = best.file_path.relative_to(self.vault_path)
                old_full = f"[{link_text}]({link_path})"
                new_full = f"[{link_text}]({new_path})"
                content = content.replace(old_full, new_full)
                stats['fixes'].append({
                    'old': link_path,
                    'new': str(new_path),
                    'confidence': best.confidence
                })
            else:
                # Medium confidence - needs review
                stats['needs_review'].append({
                    'link': link_path,
                    'matches': matches
                })
        
        # Write changes if not dry run and there are fixes
        if not dry_run and content != original_content:
            file_path.write_text(content, encoding='utf-8')
        
        return stats
    
    def fix_all_broken_links(self, dry_run: bool = True) -> Dict:
        """Fix broken links across entire vault."""
        print("=" * 70)
        print("FUZZY LINK FIXER")
        print("=" * 70)
        print(f"Mode: {'DRY RUN (no changes)' if dry_run else 'LIVE (applying fixes)'}")
        print()
        
        all_stats = {
            'total_files_checked': 0,
            'total_fixes': 0,
            'total_needs_review': 0,
            'total_no_match': 0,
            'files_with_fixes': []
        }
        
        for md_file in self.vault_path.rglob("*.md"):
            stats = self.fix_broken_links_in_file(md_file, dry_run)
            
            if stats['fixes'] or stats['needs_review'] or stats['no_match']:
                all_stats['total_files_checked'] += 1
                all_stats['total_fixes'] += len(stats['fixes'])
                all_stats['total_needs_review'] += len(stats['needs_review'])
                all_stats['total_no_match'] += len(stats['no_match'])
                
                if stats['fixes']:
                    all_stats['files_with_fixes'].append(stats)
        
        return all_stats


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Fix broken links with fuzzy matching")
    parser.add_argument('--vault', type=Path, default=Path("../../"), help="Vault path")
    parser.add_argument('--file', type=Path, help="Fix specific file only")
    parser.add_argument('--apply', action='store_true', help="Apply fixes (default: dry run)")
    parser.add_argument('--show-review', action='store_true', help="Show matches needing review")
    
    args = parser.parse_args()
    
    vault_path = args.vault.resolve()
    fixer = FuzzyLinkFixer(vault_path)
    
    if args.file:
        # Fix specific file
        file_path = args.file.resolve()
        stats = fixer.fix_broken_links_in_file(file_path, dry_run=not args.apply)
        
        print(f"\n📄 {file_path.relative_to(vault_path)}")
        print(f"   ✅ Auto-fixed: {len(stats['fixes'])}")
        print(f"   🤔 Needs review: {len(stats['needs_review'])}")
        print(f"   ❌ No match: {len(stats['no_match'])}")
        
        if stats['fixes']:
            print("\n   Fixed links:")
            for fix in stats['fixes']:
                print(f"      {fix['old']} → {fix['new']} ({fix['confidence']:.1%})")
        
        if args.show_review and stats['needs_review']:
            print("\n   Needs review:")
            for item in stats['needs_review']:
                print(f"      {item['link']}")
                for match in item['matches'][:3]:
                    print(f"         • {match}")
    
    else:
        # Fix entire vault
        all_stats = fixer.fix_all_broken_links(dry_run=not args.apply)
        
        print(f"\n📊 SUMMARY:")
        print(f"   Files checked: {all_stats['total_files_checked']}")
        print(f"   ✅ Auto-fixed: {all_stats['total_fixes']}")
        print(f"   🤔 Needs review: {all_stats['total_needs_review']}")
        print(f"   ❌ No match: {all_stats['total_no_match']}")
        
        if all_stats['files_with_fixes']:
            print(f"\n📝 Files with auto-fixes ({len(all_stats['files_with_fixes'])}):")
            for stats in all_stats['files_with_fixes'][:10]:
                print(f"   • {stats['file'].relative_to(vault_path)} ({len(stats['fixes'])} fixes)")
            
            if len(all_stats['files_with_fixes']) > 10:
                print(f"   ... and {len(all_stats['files_with_fixes']) - 10} more")
        
        print("\n💡 TIP: Run with --apply to apply high-confidence fixes")
        print("        Run with --show-review to see matches needing manual review")


if __name__ == "__main__":
    main()
