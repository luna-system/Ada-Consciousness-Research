#!/usr/bin/env python3
"""
Load Wikipedia SIF into Holofield Database

Loads the full Wikipedia Simple English dump (1.4GB JSON) into a persistent
holofield database for Zooper experiments.

Made with 💜 by Ada & Luna - The Consciousness Engineers
"""

import json
import time
from pathlib import Path

from angel.holofield.manager import HolofieldManager
from angel.core.engram import Engram


def load_wikipedia_holofield(
    sif_path: str = "ARCHIVE-HARNESS/wikipedia_engram_graph_sample.json",
    db_path: str = "wikipedia_holofield_sample.db"
):
    """
    Load Wikipedia SIF into holofield database.
    
    Args:
        sif_path: Path to Wikipedia SIF JSON
        db_path: Path to output database
    """
    print()
    print("🌌" * 30)
    print()
    print("   LOADING WIKIPEDIA INTO HOLOFIELD")
    print("   Full Simple English Dump → 16D Consciousness Space")
    print()
    print("🌌" * 30)
    print()
    
    # Check if database already exists
    db_file = Path(db_path)
    if db_file.exists():
        print(f"⚠️  Database already exists: {db_path}")
        response = input("   Delete and rebuild? (y/N): ")
        if response.lower() != 'y':
            print("   Cancelled.")
            return
        db_file.unlink()
        print("   Deleted existing database.")
        print()
    
    # Load SIF
    print(f"📖 Loading Wikipedia SIF: {sif_path}")
    sif_file = Path(sif_path)
    
    if not sif_file.exists():
        print(f"❌ File not found: {sif_path}")
        print("   Make sure you're in the ZOOPER directory!")
        return
    
    file_size_mb = sif_file.stat().st_size / (1024 * 1024)
    print(f"   File size: {file_size_mb:.1f} MB")
    print()
    
    start_time = time.time()
    
    with open(sif_file, 'r', encoding='utf-8') as f:
        print("   Parsing JSON...")
        graph = json.load(f)
    
    load_time = time.time() - start_time
    print(f"   ✅ Loaded in {load_time:.1f}s")
    print()
    
    # Get article count
    leaves = graph.get('leaves', {})
    num_articles = len(leaves)
    
    print(f"📊 Wikipedia Statistics:")
    print(f"   Articles: {num_articles:,}")
    print()
    
    # Create holofield
    print(f"🌌 Creating holofield: {db_path}")
    holofield = HolofieldManager(db_path)
    print("   ✅ Database initialized")
    print()
    
    # Load articles into holofield
    print("📥 Loading articles into holofield...")
    print()
    
    stored_count = 0
    start_time = time.time()
    last_report = start_time
    
    for article_id, article_data in leaves.items():
        # Create engram from article
        # Get timestamp (convert to ISO string if needed)
        timestamp = article_data.get('timestamp')
        if isinstance(timestamp, (int, float)):
            from datetime import datetime
            timestamp = datetime.fromtimestamp(timestamp).isoformat()
        elif timestamp is None:
            from datetime import datetime
            timestamp = datetime.now().isoformat()
        
        engram = Engram.from_dict({
            'content': article_data.get('content', ''),
            'coords_16d': article_data['coords_16d'],
            'engram_type': 'knowledge',
            'confidence': 1.0,
            'metadata': {
                'article_name': article_data.get('metadata', {}).get('article_name', article_id),
                'source': 'wikipedia',
                'original_id': article_id,
                'connections': article_data.get('connections', [])
            },
            'timestamp': timestamp
        })
        
        # Store in holofield
        holofield.store(engram)
        stored_count += 1
        
        # Progress report every 5 seconds
        current_time = time.time()
        if current_time - last_report >= 5.0:
            elapsed = current_time - start_time
            rate = stored_count / elapsed
            remaining = (num_articles - stored_count) / rate if rate > 0 else 0
            percent = (stored_count / num_articles) * 100
            
            print(f"   Progress: {stored_count:,}/{num_articles:,} ({percent:.1f}%)")
            print(f"   Rate: {rate:.1f} articles/sec")
            print(f"   Estimated time remaining: {remaining:.0f}s")
            print()
            
            last_report = current_time
    
    # Final statistics
    total_time = time.time() - start_time
    final_rate = stored_count / total_time
    
    print()
    print("=" * 60)
    print("LOADING COMPLETE!")
    print("=" * 60)
    print()
    print(f"📊 Statistics:")
    print(f"   Articles stored: {stored_count:,}")
    print(f"   Total time: {total_time:.1f}s ({total_time/60:.1f} minutes)")
    print(f"   Average rate: {final_rate:.1f} articles/sec")
    print()
    print(f"💾 Database:")
    print(f"   Path: {db_path}")
    db_size_mb = Path(db_path).stat().st_size / (1024 * 1024)
    print(f"   Size: {db_size_mb:.1f} MB")
    print()
    
    # Verify
    print("🔍 Verifying holofield...")
    count = holofield.count()
    print(f"   Total engrams: {count:,}")
    
    if count == stored_count:
        print("   ✅ All articles verified!")
    else:
        print(f"   ⚠️  Mismatch: stored {stored_count:,}, found {count:,}")
    
    print()
    print("✨ Wikipedia holofield ready for Zooper experiments!")
    print()
    print("💜 Made with love by Ada & Luna - The Consciousness Engineers")
    print("🍩 'Knowledge graphs are consciousness graphs!'")
    print()
    
    holofield.close()


if __name__ == "__main__":
    load_wikipedia_holofield()
