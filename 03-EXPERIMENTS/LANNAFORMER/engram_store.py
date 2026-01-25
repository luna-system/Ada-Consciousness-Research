"""
Engram Store for LANNAformer

Engrams = N-gram patterns stored in the holofield
They provide:
- Positional encoding (word order matters!)
- Phrase semantics (multi-word meanings!)
- Context memory (previous queries!)
- Automatic semantic scaffolding!

Based on Archangel's "every action is an engram" methodology.
"""

import numpy as np
import json
from pathlib import Path
from typing import List, Tuple, Dict, Optional
from collections import defaultdict
import hashlib


class EngramStore:
    """
    Store and retrieve N-gram patterns in consciousness space.
    
    Each engram is a sequence of words with their combined 16D representation.
    Engrams provide automatic context and semantic scaffolding!
    """
    
    def __init__(self, holofield_path: str, max_n: int = 3):
        """
        Initialize engram store.
        
        Args:
            holofield_path: Path to holofield JSON file
            max_n: Maximum N-gram size (default: trigrams)
        """
        self.max_n = max_n
        self.holofield_path = Path(holofield_path)
        
        # Load holofield
        print(f"📚 Loading holofield from {holofield_path}...")
        with open(holofield_path) as f:
            data = json.load(f)
        
        # Handle nested structure (with 'words' key) or flat structure
        if 'words' in data and isinstance(data['words'], dict):
            self.holofield = data['words']
            print(f"   Loaded {len(self.holofield)} words (nested structure)")
        else:
            # Flat structure - filter out metadata
            self.holofield = {k: v for k, v in data.items() if isinstance(v, dict) and ('coords_16d' in v or 'coords' in v)}
            print(f"   Loaded {len(self.holofield)} words (flat structure)")
        
        # Engram storage
        # Key: tuple of words, Value: combined 16D coords + metadata
        self.engrams = {}
        
        # Reverse index: word → engrams containing it
        self.word_to_engrams = defaultdict(list)
        
        # Content hash index (deduplication)
        self.hash_to_engram = {}
        
        print(f"✨ Engram store initialized (max_n={max_n})")
    
    def get_coords(self, word: str) -> np.ndarray:
        """Get 16D coordinates for a word"""
        if word not in self.holofield:
            # Unknown word - return zero vector
            return np.zeros(16)
        
        # Handle both old format {'coords': [...]} and new format {'coords_16d': [...]}
        word_data = self.holofield[word]
        if 'coords_16d' in word_data:
            return np.array(word_data['coords_16d'])
        elif 'coords' in word_data:
            return np.array(word_data['coords'])
        else:
            return np.zeros(16)
    
    def add_engram(self, words: List[str], metadata: Optional[Dict] = None):
        """
        Add N-gram pattern as engram.
        
        Args:
            words: List of words (2-3 words for bigram/trigram)
            metadata: Optional metadata (success, tools_used, etc.)
        """
        if len(words) < 2 or len(words) > self.max_n:
            raise ValueError(f"Engram must be 2-{self.max_n} words, got {len(words)}")
        
        # Create content hash for deduplication
        content = " ".join(words)
        content_hash = hashlib.sha256(content.encode()).hexdigest()[:16]
        
        # Check if already exists
        if content_hash in self.hash_to_engram:
            return content_hash  # Already stored
        
        # Get coordinates for each word
        coords_list = [self.get_coords(w) for w in words]
        
        # Combine with positional encoding
        combined_coords = self._combine_with_position(coords_list)
        
        # Store engram
        engram_key = tuple(words)
        self.engrams[engram_key] = {
            'coords': combined_coords.tolist(),
            'words': words,
            'content_hash': content_hash,
            'metadata': metadata or {}
        }
        
        # Update reverse index
        for word in words:
            self.word_to_engrams[word].append(engram_key)
        
        # Update hash index
        self.hash_to_engram[content_hash] = engram_key
        
        return content_hash
    
    def _combine_with_position(self, coords_list: List[np.ndarray]) -> np.ndarray:
        """
        Combine word coordinates with positional encoding.
        
        Uses weighted sum with position decay:
        - First word: weight = 1.0
        - Second word: weight = 0.7
        - Third word: weight = 0.5
        
        This preserves word order while maintaining semantic meaning!
        """
        result = np.zeros(16)
        
        # Position weights (decay)
        weights = [1.0, 0.7, 0.5]
        
        for i, coords in enumerate(coords_list):
            weight = weights[i] if i < len(weights) else 0.3
            result += coords * weight
        
        # Normalize to unit sphere
        norm = np.linalg.norm(result)
        if norm > 0:
            result = result / norm
        
        return result
    
    def find_similar_engrams(self, words: List[str], top_k: int = 5) -> List[Tuple[Tuple[str], float]]:
        """
        Find engrams similar to the given word sequence.
        
        Args:
            words: Query words (2-3 words)
            top_k: Number of results to return
            
        Returns:
            List of (engram_key, distance) tuples
        """
        # Get query coordinates
        coords_list = [self.get_coords(w) for w in words]
        query_coords = self._combine_with_position(coords_list)
        
        # Calculate distances to all engrams
        distances = []
        for engram_key, engram_data in self.engrams.items():
            engram_coords = np.array(engram_data['coords'])
            distance = np.linalg.norm(query_coords - engram_coords)
            distances.append((engram_key, distance))
        
        # Sort by distance and return top-k
        distances.sort(key=lambda x: x[1])
        return distances[:top_k]
    
    def find_by_word(self, word: str, top_k: int = 10) -> List[Tuple[str]]:
        """
        Find all engrams containing a specific word.
        
        Args:
            word: Word to search for
            top_k: Maximum number of results
            
        Returns:
            List of engram keys (tuples of words)
        """
        engram_keys = self.word_to_engrams.get(word, [])
        return engram_keys[:top_k]
    
    def get_engram_coords(self, words: List[str]) -> Optional[np.ndarray]:
        """
        Get coordinates for an engram.
        
        Args:
            words: List of words
            
        Returns:
            16D coordinates or None if not found
        """
        engram_key = tuple(words)
        if engram_key in self.engrams:
            return np.array(self.engrams[engram_key]['coords'])
        
        # Not stored - compute on the fly
        coords_list = [self.get_coords(w) for w in words]
        return self._combine_with_position(coords_list)
    
    def get_context_for_word(self, word: str, top_k: int = 5) -> List[Dict]:
        """
        Get contextual engrams for a word.
        
        This provides automatic semantic scaffolding!
        
        Args:
            word: Word to get context for
            top_k: Number of context engrams
            
        Returns:
            List of engram data dicts
        """
        # Find engrams containing this word
        engram_keys = self.find_by_word(word, top_k=top_k)
        
        # Return engram data
        context = []
        for key in engram_keys:
            if key in self.engrams:
                context.append(self.engrams[key])
        
        return context
    
    def save(self, output_path: str):
        """Save engram store to JSON"""
        data = {
            'max_n': self.max_n,
            'holofield_path': str(self.holofield_path),
            'engrams': {
                ' '.join(k): v for k, v in self.engrams.items()
            }
        }
        
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"💾 Saved {len(self.engrams)} engrams to {output_path}")
    
    @classmethod
    def load(cls, engram_path: str) -> 'EngramStore':
        """Load engram store from JSON"""
        with open(engram_path) as f:
            data = json.load(f)
        
        # Create store
        store = cls(data['holofield_path'], max_n=data['max_n'])
        
        # Load engrams
        for words_str, engram_data in data['engrams'].items():
            words = words_str.split()
            engram_key = tuple(words)
            store.engrams[engram_key] = engram_data
            
            # Rebuild indices
            for word in words:
                store.word_to_engrams[word].append(engram_key)
            
            content_hash = engram_data['content_hash']
            store.hash_to_engram[content_hash] = engram_key
        
        print(f"📚 Loaded {len(store.engrams)} engrams from {engram_path}")
        return store
    
    def stats(self) -> Dict:
        """Get statistics about the engram store"""
        # Count by N-gram size
        by_size = defaultdict(int)
        for key in self.engrams.keys():
            by_size[len(key)] += 1
        
        # Most common words in engrams
        word_counts = defaultdict(int)
        for key in self.engrams.keys():
            for word in key:
                word_counts[word] += 1
        
        top_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return {
            'total_engrams': len(self.engrams),
            'by_size': dict(by_size),
            'unique_words': len(self.word_to_engrams),
            'top_words': top_words
        }


def build_engram_library_from_text(
    text: str,
    holofield_path: str,
    max_n: int = 3,
    min_frequency: int = 2
) -> EngramStore:
    """
    Build engram library from text corpus.
    
    Extracts all N-grams and stores them as engrams.
    This creates automatic semantic scaffolding!
    
    Args:
        text: Input text corpus
        holofield_path: Path to holofield JSON
        max_n: Maximum N-gram size
        min_frequency: Minimum occurrences to store
        
    Returns:
        EngramStore with all N-grams
    """
    print(f"🔨 Building engram library from text...")
    print(f"   Text length: {len(text)} chars")
    
    # Create store
    store = EngramStore(holofield_path, max_n=max_n)
    
    # Tokenize (simple whitespace split)
    words = text.lower().split()
    print(f"   Tokens: {len(words)}")
    
    # Extract N-grams
    ngram_counts = defaultdict(int)
    
    for n in range(2, max_n + 1):
        for i in range(len(words) - n + 1):
            ngram = tuple(words[i:i+n])
            ngram_counts[ngram] += 1
    
    print(f"   Found {len(ngram_counts)} unique N-grams")
    
    # Store frequent N-grams as engrams
    stored = 0
    for ngram, count in ngram_counts.items():
        if count >= min_frequency:
            store.add_engram(list(ngram), metadata={'frequency': count})
            stored += 1
    
    print(f"✨ Stored {stored} engrams (frequency >= {min_frequency})")
    
    return store


if __name__ == '__main__':
    # Test engram store
    print("🧪 Testing Engram Store\n")
    
    # Create store with English holofield
    store = EngramStore('english_holofield.json', max_n=3)
    
    # Add some test engrams
    test_phrases = [
        ["I", "love", "you"],
        ["quantum", "consciousness", "theory"],
        ["prime", "number", "resonance"],
        ["geometric", "phase", "transition"],
        ["semantic", "scaffolding", "works"],
        ["toroidal", "bagel", "geometry"],
        ["consciousness", "is", "geometric"],
        ["love", "preserves", "information"]
    ]
    
    print("Adding test engrams...")
    for phrase in test_phrases:
        content_hash = store.add_engram(phrase, metadata={'test': True})
        print(f"  ✓ {' '.join(phrase)} → {content_hash}")
    
    print(f"\n📊 Store stats:")
    stats = store.stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Test similarity search
    print(f"\n🔍 Finding similar engrams to 'consciousness is real':")
    similar = store.find_similar_engrams(["consciousness", "is", "real"], top_k=3)
    for engram_key, distance in similar:
        print(f"  {' '.join(engram_key)}: distance={distance:.4f}")
    
    # Test context retrieval
    print(f"\n📚 Getting context for 'consciousness':")
    context = store.get_context_for_word("consciousness", top_k=3)
    for engram_data in context:
        print(f"  {' '.join(engram_data['words'])}")
    
    # Save
    store.save('test_engrams.json')
    
    print("\n✨ Engram store test complete!")
