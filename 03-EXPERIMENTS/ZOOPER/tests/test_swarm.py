"""
Test ZooperSwarm - The attention mechanism!

Made with 💜 by Ada & Luna - The Consciousness Engineers
"""

import pytest
import tempfile
from pathlib import Path

from zooper import ZooperSwarm
from angel.holofield.manager import HolofieldManager


@pytest.fixture
def holofield():
    """Create temporary holofield for testing."""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        db_path = f.name
    
    holofield = HolofieldManager(db_path)
    yield holofield
    
    # Cleanup
    holofield.close()
    Path(db_path).unlink(missing_ok=True)


@pytest.fixture
def swarm(holofield):
    """Create ZooperSwarm for testing."""
    return ZooperSwarm(holofield, num_zooperlings=13)


@pytest.fixture
def sample_article():
    """Sample Wikipedia article for testing."""
    return {
        'content': 'April is the fourth month of the year. It has 30 days. '
                   'April comes after March and before May. '
                   'The name April comes from the Latin word aperire, which means to open.',
        'metadata': {
            'article_name': 'April',
            'source': 'wikipedia'
        }
    }


def test_swarm_initialization(swarm):
    """Test that swarm initializes correctly."""
    assert swarm.num_zooperlings == 13
    assert len(swarm.zooperlings) == 13
    assert swarm.eve_fleet is not None
    assert swarm.kuramoto is not None
    assert swarm.edge_weights is not None


def test_swarm_inherits_engram_creator(swarm):
    """Test that ZooperSwarm properly inherits from EngramCreator."""
    from angel.core.engram_creator import EngramCreator
    assert isinstance(swarm, EngramCreator)
    
    # Check required methods exist
    assert hasattr(swarm, 'process')
    assert hasattr(swarm, 'to_16d')
    assert hasattr(swarm, 'create_engram')
    assert hasattr(swarm, 'store_engram')


def test_article_decomposition(swarm, sample_article):
    """Test parallel decomposition of article."""
    decomposition = swarm.parallel_decompose(sample_article)
    
    # Check structure
    assert 1 in decomposition  # Words
    assert 2 in decomposition  # Bigrams
    assert 3 in decomposition  # Trigrams
    
    # Check content
    words = decomposition[1]
    assert len(words) > 0
    assert 'april' in words
    assert 'month' in words
    
    bigrams = decomposition[2]
    assert len(bigrams) > 0
    
    trigrams = decomposition[3]
    assert len(trigrams) > 0


def test_process_creates_engrams(swarm, sample_article, holofield):
    """Test that process() creates engrams in holofield."""
    # Get initial count
    initial_count = holofield.count()
    
    # Process article
    decomposition, article_engram = swarm.process(sample_article)
    
    # Check article engram
    assert article_engram is not None
    assert article_engram.content == sample_article['content']
    assert article_engram.engram_type == 'knowledge'
    assert len(article_engram.coords_16d) == 16
    
    # Check engrams were stored
    final_count = holofield.count()
    assert final_count > initial_count
    
    # Check decomposition results
    assert len(decomposition[1]) > 0  # Words found


def test_to_16d_mapping(swarm, sample_article):
    """Test that articles map to 16D coordinates."""
    coords = swarm.to_16d(sample_article)
    
    assert coords is not None
    assert len(coords) == 16
    assert coords.dtype == float


def test_hebbian_edge_creation(swarm, sample_article):
    """Test that Hebbian edges are created."""
    # Process article
    decomposition, article_engram = swarm.process(sample_article)
    
    # Check edge weights were created
    stats = swarm.edge_weights.get_statistics()
    assert stats['total_edges'] > 0
    assert stats['mean_weight'] > 0


def test_eve_fleet_broadcast(swarm, sample_article):
    """Test EVE Fleet broadcasting."""
    # Decompose article
    decomposition = swarm.parallel_decompose(sample_article)
    
    # Check that discoveries were shared
    # (broadcast happens during parallel_decompose)
    popular = swarm.eve_fleet.get_popular_discoveries(top_k=5)
    assert len(popular) > 0
    
    # Check that multiple zooperlings found common words
    for word, count in popular:
        assert count > 0


def test_kuramoto_coherence(swarm):
    """Test Kuramoto dynamics."""
    # Get initial coherence
    r, psi = swarm.kuramoto.order_parameter()
    
    assert 0.0 <= r <= 1.0
    assert -3.15 <= psi <= 3.15  # Approximately -π to π
    
    # Get navigation mode
    mode = swarm.kuramoto.get_coherence_mode()
    assert mode in ["LOCAL", "GLOBAL", "ADAPTIVE"]


def test_swarm_statistics(swarm, sample_article):
    """Test swarm statistics."""
    # Process article
    swarm.process(sample_article)
    
    # Get statistics
    stats = swarm.get_statistics()
    
    assert 'num_zooperlings' in stats
    assert stats['num_zooperlings'] == 13
    
    assert 'total_discoveries' in stats
    assert stats['total_discoveries'] > 0
    
    assert 'avg_confidence' in stats
    assert 0.0 <= stats['avg_confidence'] <= 1.0
    
    assert 'kuramoto_coherence' in stats
    assert 0.0 <= stats['kuramoto_coherence'] <= 1.0


def test_zooperling_decomposition(swarm, sample_article):
    """Test individual zooperling decomposition."""
    zooper = swarm.zooperlings[0]
    
    ngrams = zooper.decompose(sample_article)
    
    assert 1 in ngrams
    assert 2 in ngrams
    assert 3 in ngrams
    
    # Check discoveries were tracked
    assert len(zooper.discoveries) > 0


def test_eve_fleet_search(swarm, sample_article):
    """Test EVE Fleet search across swarm."""
    # Process article (triggers broadcasts)
    swarm.parallel_decompose(sample_article)
    
    # Search for a word we know exists
    results = swarm.eve_fleet.search('april')
    
    # Should find matches
    assert len(results) > 0


def test_multiple_articles(swarm, holofield):
    """Test processing multiple articles."""
    articles = [
        {
            'content': 'April is the fourth month.',
            'metadata': {'article_name': 'April'}
        },
        {
            'content': 'May is the fifth month.',
            'metadata': {'article_name': 'May'}
        },
        {
            'content': 'June is the sixth month.',
            'metadata': {'article_name': 'June'}
        }
    ]
    
    for article in articles:
        decomposition, engram = swarm.process(article)
        assert engram is not None
    
    # Check all engrams were stored
    assert holofield.count() >= len(articles)
    
    # Check edge weights accumulated
    stats = swarm.edge_weights.get_statistics()
    assert stats['total_edges'] > 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
