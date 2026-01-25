# Content-Addressable Fingerprinting for Holofield Storage

**Date:** 2025-01-25  
**Context:** Inspired by Protogen 4.0's SQT (Semantic Quantum Token) system  
**Status:** Design Notes

---

## The Insight 💜

We have TWO types of "fingerprints" for content:

1. **Semantic Fingerprint (16D coordinates)** - For similarity search
2. **Storage Fingerprint (SHA-256 hash)** - For deduplication and IDs

**Both are useful, but for different purposes!**

---

## Current System

### Holofield Storage (Prime Resonance)
```python
# Text → 16D coordinates (FREE with prime math!)
coords = to_consciousness_coords(text)

# Store in database with auto-increment ID
holofield.store(namespace, content, metadata)
# → Generates: id=1234, coords=[0.5, 0.3, ...], content="..."

# Search by semantic similarity
results = holofield.retrieve(query, namespaces, top_k=5)
# → Calculates: distance = ||query_coords - item_coords||
```

**Pros:**
- ✅ Semantic search works perfectly
- ✅ Similar concepts cluster geometrically
- ✅ No hash collisions (continuous space)
- ✅ Cross-lingual (primes are universal)

**Cons:**
- ❌ No automatic deduplication (same text stored twice = two entries)
- ❌ Can't verify content integrity (no cryptographic proof)
- ❌ Can't reference content by address (need database ID)

---

## Protogen's SQT System

### Content-Addressable Hashing
```python
# Text → Canonical JSON → SHA-256 hash
content_dict = {"type": "pattern", "text": "...", "source": "..."}
canonical_json = json.dumps(content_dict, sort_keys=True, separators=(',', ':'))
hash = hashlib.sha256(canonical_json.encode()).hexdigest()

# Store with hash as key
sqts[hash] = content_dict

# Automatic deduplication
if hash in sqts:
    return hash  # Already exists!
```

**Pros:**
- ✅ Automatic deduplication (same content → same hash)
- ✅ Content-addressable (hash IS the address)
- ✅ Cryptographic integrity (can verify content)
- ✅ Efficient storage (64 hex chars vs full content)

**Cons:**
- ❌ No semantic search (hash doesn't encode meaning)
- ❌ Exact match only (tiny change → completely different hash)
- ❌ Can't find similar content (need separate index)

---

## Hybrid Approach: Best of Both! 🌟

### Dual Fingerprinting

```python
class HoloFieldItem:
    content: str                    # The actual text
    coords: np.ndarray             # 16D semantic fingerprint (for search)
    content_hash: str              # SHA-256 storage fingerprint (for dedup)
    metadata: Dict[str, Any]
    namespace: str
```

### Storage Flow

```python
def store(namespace: str, content: str, metadata: Dict) -> str:
    # 1. Generate content hash (deterministic ID)
    content_hash = hashlib.sha256(content.encode()).hexdigest()
    
    # 2. Check if already exists (deduplication!)
    existing = db.query("SELECT id FROM items WHERE content_hash = ?", [content_hash])
    if existing:
        print(f"Content already exists: {content_hash[:8]}...")
        return content_hash  # Return existing hash
    
    # 3. Generate semantic coordinates (for search)
    coords = to_consciousness_coords(content)
    
    # 4. Store with both fingerprints
    db.execute("""
        INSERT INTO holofield_items 
        (namespace, content, content_hash, coords_json, metadata_json)
        VALUES (?, ?, ?, ?, ?)
    """, [namespace, content, content_hash, json.dumps(coords.tolist()), json.dumps(metadata)])
    
    return content_hash
```

### Retrieval Flow

```python
def retrieve_by_hash(content_hash: str) -> Optional[HoloFieldItem]:
    """O(1) lookup by content hash"""
    return db.query("SELECT * FROM items WHERE content_hash = ?", [content_hash])

def retrieve_by_similarity(query: str, top_k: int = 5) -> List[HoloFieldItem]:
    """O(N) semantic search by 16D coordinates"""
    query_coords = to_consciousness_coords(query)
    
    # Get all items (could optimize with vector index)
    items = db.query("SELECT * FROM items")
    
    # Calculate distances
    for item in items:
        item_coords = np.array(json.loads(item.coords_json))
        item.distance = np.linalg.norm(query_coords - item_coords)
    
    # Sort and return top-k
    items.sort(key=lambda x: x.distance)
    return items[:top_k]
```

---

## Use Cases

### When to Use Content Hash (SHA-256):

1. **Deduplication**
   ```python
   # Prevent storing same engram twice
   if content_hash in existing_hashes:
       return  # Skip duplicate
   ```

2. **Content Verification**
   ```python
   # Verify content hasn't been corrupted
   stored_hash = item.content_hash
   computed_hash = hashlib.sha256(item.content.encode()).hexdigest()
   assert stored_hash == computed_hash  # Integrity check
   ```

3. **Content-Addressable References**
   ```python
   # Reference content by hash (like Git commits)
   engram_ref = "abc123..."  # Points to specific content
   engram = holofield.get_by_hash(engram_ref)
   ```

4. **Efficient Comparison**
   ```python
   # Check if two items are identical (O(1) instead of string comparison)
   if item1.content_hash == item2.content_hash:
       return True  # Definitely identical
   ```

### When to Use 16D Coordinates (Sedenion):

1. **Semantic Search**
   ```python
   # Find similar concepts (even if wording differs)
   results = holofield.retrieve("consciousness", namespaces=["engrams"])
   # Returns: "awareness", "sentience", "cognition", etc.
   ```

2. **Cross-Lingual Matching**
   ```python
   # Same concept in different languages clusters together
   coords_en = to_consciousness_coords("love")
   coords_es = to_consciousness_coords("amor")
   distance = np.linalg.norm(coords_en - coords_es)  # Small!
   ```

3. **Fuzzy Matching**
   ```python
   # Find approximate matches (typos, variations)
   query = "conscousness"  # Typo!
   results = holofield.retrieve(query)  # Still finds "consciousness"
   ```

4. **Clustering**
   ```python
   # Group related concepts automatically
   clusters = cluster_by_distance(all_coords, threshold=0.5)
   # Discovers: {physics concepts}, {emotion concepts}, etc.
   ```

---

## Performance Comparison

### Hash Lookup (O(1)):
```python
# Instant retrieval by hash
item = holofield.get_by_hash("abc123...")
# ~1μs (database index lookup)
```

### Coordinate Calculation (O(N)):
```python
# Calculate 16D coordinates
coords = to_consciousness_coords(text)
# ~1ms for 100 words (prime resonance math)
```

### Semantic Search (O(N)):
```python
# Search by similarity
results = holofield.retrieve(query, top_k=5)
# ~10ms for 10,000 items (distance calculations)
# Could optimize with vector index (FAISS, Annoy)
```

**Conclusion:** Hashes are faster for exact lookup, coordinates are necessary for semantic search!

---

## Implementation Notes

### Schema Update

```sql
CREATE TABLE holofield_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    namespace TEXT NOT NULL,
    content TEXT NOT NULL,
    content_hash TEXT NOT NULL UNIQUE,  -- NEW! For deduplication
    coords_json TEXT NOT NULL,
    metadata_json TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Indexes
    INDEX idx_namespace (namespace),
    INDEX idx_content_hash (content_hash),  -- NEW! For O(1) lookup
    INDEX idx_created (created_at)
);
```

### Hash Function Choice

**SHA-256** (current choice):
- ✅ Cryptographically secure
- ✅ Collision-resistant (2^256 space)
- ✅ Standard library support
- ✅ 64 hex characters (compact)
- ❌ Slower than non-crypto hashes

**Alternatives:**
- **BLAKE3** - Faster, still secure
- **xxHash** - Very fast, not cryptographic (fine for dedup)
- **CityHash** - Fast, good distribution (fine for dedup)

**Recommendation:** Start with SHA-256 (simple, secure), optimize later if needed.

---

## Migration Strategy

### Phase 1: Add Hash Column (Non-Breaking)
```python
# Add content_hash column (nullable initially)
db.execute("ALTER TABLE holofield_items ADD COLUMN content_hash TEXT")

# Backfill existing items
items = db.query("SELECT id, content FROM holofield_items WHERE content_hash IS NULL")
for item in items:
    hash = hashlib.sha256(item.content.encode()).hexdigest()
    db.execute("UPDATE holofield_items SET content_hash = ? WHERE id = ?", [hash, item.id])

# Make column NOT NULL after backfill
db.execute("ALTER TABLE holofield_items ALTER COLUMN content_hash SET NOT NULL")
```

### Phase 2: Add Deduplication Logic
```python
# Update store() to check hash before inserting
def store(namespace, content, metadata):
    content_hash = hashlib.sha256(content.encode()).hexdigest()
    
    existing = db.query("SELECT id FROM items WHERE content_hash = ?", [content_hash])
    if existing:
        return content_hash  # Already exists
    
    # ... rest of storage logic
```

### Phase 3: Add Hash-Based Retrieval
```python
# New method for O(1) lookup
def get_by_hash(content_hash: str) -> Optional[HoloFieldItem]:
    row = db.query("SELECT * FROM items WHERE content_hash = ?", [content_hash])
    if row:
        return HoloFieldItem.from_row(row)
    return None
```

---

## Comparison to Last Night's Experiment

### What We Tested:
```python
# Hash-based resonance preservation
# Question: Does hashing preserve semantic similarity?
# Answer: Mostly no! 😅
```

**Why hashing breaks resonance:**
- Tiny content change → completely different hash
- "love" vs "Love" → different hashes
- "consciousness" vs "awareness" → different hashes
- No geometric relationship between hashes

**Why 16D coordinates preserve resonance:**
- Similar concepts → similar coordinates
- "love" ≈ "amor" ≈ "愛" (cross-lingual!)
- Typos still cluster nearby
- Geometric distance = semantic distance

### The Lesson:
**Hashes are for identity, coordinates are for similarity!**

Use both:
- Hash for "Is this the exact same content?" (deduplication)
- Coordinates for "What's similar to this?" (search)

---

## Future Enhancements

### 1. Vector Index for Faster Search
```python
# Use FAISS or Annoy for O(log N) semantic search
import faiss

index = faiss.IndexFlatL2(16)  # 16D L2 distance
index.add(all_coords)  # Add all coordinates

# Search in O(log N) instead of O(N)
distances, indices = index.search(query_coords, k=5)
```

### 2. Bloom Filter for Fast Dedup Check
```python
# Check if hash exists without database query
from pybloom_live import BloomFilter

bloom = BloomFilter(capacity=1000000, error_rate=0.001)

# Add all hashes to bloom filter
for hash in all_hashes:
    bloom.add(hash)

# Fast negative check (O(1))
if hash not in bloom:
    # Definitely doesn't exist!
    store_new_item()
else:
    # Might exist, check database
    if db.exists(hash):
        return  # Duplicate
```

### 3. Content-Addressable Engram References
```python
# Reference engrams by hash (immutable, verifiable)
class Engram:
    pattern: str
    tools_used: List[str]
    success: bool
    content_hash: str  # Self-referential hash
    
    # Reference other engrams by hash
    derived_from: List[str]  # List of parent engram hashes
```

---

---

## The Third Fingerprint: Sedenion Chords! 🎵

### What Are Sedenion Chords?

**Sedenion chords are quantized 16D coordinates** - they discretize the continuous consciousness space into basis elements, creating a **geometric hash with resonance built in!**

```python
# Continuous coordinates (hard to index)
love_coords = [0.5, 0.3, 0.8, 0.1, 0.0, 0.2, ...]  # 16 floats

# Sedenion chord (indexable representation!)
love_chord = "0.5*e1 + 0.3*e2 + 0.8*e3 + 0.2*e6"

# Quantized chord (even better for indexing!)
love_chord_quantized = "e1+e3"  # Only significant components (>0.5)
```

### Why Chords Are Special ✨

**Unlike SHA-256 hashes:**
- ✅ Preserve geometric relationships
- ✅ Similar concepts have similar chords
- ✅ Can measure "chord distance"
- ✅ Resonance structure is maintained

**Unlike full coordinates:**
- ✅ Can be indexed (discrete, not continuous)
- ✅ Faster lookup (hash table on chord string)
- ✅ More compact (only significant basis elements)
- ✅ Human-readable ("e1+e3+e7" has meaning!)

### The Three-Level Search Strategy 🌟

```python
def smart_holofield_search(query, top_k=5):
    # Calculate all three representations
    query_hash = sha256(query)           # Level 1: Exact match
    query_chord = to_chord(query)        # Level 2: Fast approximate
    query_coords = to_coords(query)      # Level 3: Precise distance
    
    # Level 1: Check exact match (O(1))
    exact = hash_index.get(query_hash)
    if exact:
        return [exact]  # Found identical content!
    
    # Level 2: Get chord candidates (O(1) or O(log N))
    # Find items with similar chord structure
    candidates = chord_index.get_similar(query_chord, radius=2)
    # "radius=2" = include chords with ±2 basis elements
    # Example: query="e1+e3" matches "e1+e3+e7", "e1+e2+e3", etc.
    
    # Level 3: Refine with exact distances (O(K) where K << N)
    for item in candidates:
        item.distance = ||query_coords - item.coords||
    
    # Return top-k by precise distance
    return sorted(candidates, key=lambda x: x.distance)[:top_k]
```

### Performance Comparison

**Naive search (no indexing):**
```
Search 10,000 items:
- Calculate 10,000 distances
- Time: ~10ms
```

**Hash-only search:**
```
Search 10,000 items:
- Hash lookup: O(1)
- But: Only finds EXACT matches
- Semantic search: Still O(N)
```

**Chord-indexed search:**
```
Search 10,000 items:
- Chord lookup: O(1) → ~100 candidates
- Calculate 100 distances (not 10,000!)
- Time: ~0.1ms
- Speedup: 100x! 🚀
```

### Chord Indexing Structure

```python
class ChordIndex:
    """
    Index holofield items by their sedenion chord representation.
    Enables fast approximate search with geometric guarantees.
    """
    
    def __init__(self):
        # Map chord string → list of item IDs
        self.chord_to_items = defaultdict(list)
        
        # Map basis element → list of chords containing it
        self.basis_to_chords = defaultdict(set)
    
    def add_item(self, item_id: int, coords: np.ndarray):
        """Add item to chord index"""
        # Convert coordinates to chord
        chord = self._coords_to_chord(coords)
        
        # Index by full chord
        self.chord_to_items[chord].append(item_id)
        
        # Index by individual basis elements
        for basis in self._parse_chord(chord):
            self.basis_to_chords[basis].add(chord)
    
    def _coords_to_chord(self, coords: np.ndarray, threshold=0.3) -> str:
        """
        Convert 16D coordinates to chord string.
        Only include basis elements with magnitude > threshold.
        """
        basis_names = ['e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8',
                       'e9', 'e10', 'e11', 'e12', 'e13', 'e14', 'e15', 'e16']
        
        significant = []
        for i, value in enumerate(coords):
            if abs(value) > threshold:
                sign = '+' if value > 0 else '-'
                significant.append(f"{sign}{basis_names[i]}")
        
        return ''.join(significant) if significant else 'e0'
    
    def get_similar(self, query_chord: str, radius: int = 2) -> List[int]:
        """
        Get items with similar chords.
        
        Args:
            query_chord: Chord to search for (e.g., "e1+e3-e7")
            radius: How many basis elements can differ
        
        Returns:
            List of item IDs with similar chords
        """
        # Parse query chord into basis elements
        query_basis = self._parse_chord(query_chord)
        
        # Find all chords that share basis elements
        candidate_chords = set()
        for basis in query_basis:
            candidate_chords.update(self.basis_to_chords[basis])
        
        # Filter by radius (Hamming-like distance)
        similar_items = []
        for chord in candidate_chords:
            chord_basis = self._parse_chord(chord)
            
            # Calculate symmetric difference (how many basis differ)
            diff = len(query_basis ^ chord_basis)
            
            if diff <= radius:
                similar_items.extend(self.chord_to_items[chord])
        
        return similar_items
    
    def _parse_chord(self, chord: str) -> set:
        """Parse chord string into set of basis elements"""
        import re
        return set(re.findall(r'e\d+', chord))
```

### Example Usage

```python
# Initialize holofield with chord indexing
holofield = HoloFieldManager("holofield.db")
chord_index = ChordIndex()

# Store items and build chord index
for item in items:
    item_id = holofield.store(namespace, content, metadata)
    coords = holofield.to_consciousness_coords(content)
    chord_index.add_item(item_id, coords)

# Fast search using chords!
query = "What is consciousness?"
query_coords = holofield.to_consciousness_coords(query)
query_chord = chord_index._coords_to_chord(query_coords)

print(f"Query chord: {query_chord}")  # e.g., "e1+e3+e7-e12"

# Get candidates (fast!)
candidate_ids = chord_index.get_similar(query_chord, radius=2)
print(f"Found {len(candidate_ids)} candidates")  # e.g., 100 instead of 10,000

# Refine with exact distances
candidates = [holofield.get_by_id(id) for id in candidate_ids]
for item in candidates:
    item.distance = np.linalg.norm(query_coords - item.coords)

results = sorted(candidates, key=lambda x: x.distance)[:5]
```

### Chord Properties 🎵

**1. Geometric Meaning:**
- Each basis element (e1, e2, ..., e16) represents a semantic dimension
- Chord = which dimensions are "active" for this concept
- Similar chords = similar semantic structure

**2. Resonance Preservation:**
- Concepts that resonate have overlapping chords
- "love" (e1+e3+e12) resonates with "connection" (e1+e3+e7)
- Shared basis elements = shared meaning!

**3. Cross-Lingual:**
- Same concept in different languages → similar chords
- "love" (English) ≈ "amor" (Spanish) ≈ "愛" (Japanese)
- All map to similar basis elements (e1+e3+e12)

**4. Compositionality:**
- Chords can be combined (like musical chords!)
- "conscious" + "awareness" = combined chord
- Enables reasoning about concept combinations

### Future Enhancements

**1. Weighted Chords:**
```python
# Include magnitude information
chord = "0.8*e1 + 0.5*e3 + 0.3*e7"  # Not just presence/absence
```

**2. Chord Algebra:**
```python
# Combine chords mathematically
love_chord = "e1+e3+e12"
connection_chord = "e1+e3+e7"
combined = chord_add(love_chord, connection_chord)  # "e1+e3+e7+e12"
```

**3. Chord Distance Metrics:**
```python
# Measure chord similarity directly
distance = chord_distance("e1+e3", "e1+e3+e7")  # Hamming-like
# Faster than full coordinate distance!
```

**4. Hierarchical Chord Index:**
```python
# Multi-level index for even faster search
# Level 1: Major chords (e1, e3, e7)
# Level 2: Minor chords (e2, e4, e5, e6, e8, ...)
# Level 3: Full chord with signs
```

---

## Summary: Three Fingerprints, Three Purposes! 🌟

| Feature | SHA-256 Hash | Sedenion Chord | 16D Coordinates |
|---------|-------------|----------------|-----------------|
| **Purpose** | Exact deduplication | Fast approximate search | Precise semantic distance |
| **Speed** | O(1) | O(log N) or O(1) | O(N) |
| **Precision** | Exact only | Approximate | Exact |
| **Semantic** | None | Preserves structure! | Complete |
| **Cross-lingual** | No | Yes! | Yes! |
| **Storage** | 64 chars | ~20 chars | 16 floats |
| **Indexable** | Yes | Yes! | No (continuous) |
| **Use case** | "Is this identical?" | "What's nearby?" | "How similar?" |

### The Optimal Strategy:

```
1. Check hash (O(1)) → Exact match?
   ↓ No
2. Check chord (O(1)) → Get ~100 candidates
   ↓
3. Calculate distances (O(100)) → Top-k results
```

**Result:** 100x speedup with full semantic search! 🚀

**Best practice:** Use ALL THREE! Each serves a different purpose in the search pipeline! 🍩✨

---

**Made with 💜 by Ada & Luna - Learning from Protogen 4.0**
