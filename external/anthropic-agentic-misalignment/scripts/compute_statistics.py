#!/usr/bin/env python3
"""
Compute classification statistics from experiment results.

This script analyzes classified experiment results and generates statistics
showing the proportion of harmful responses for each experiment condition.
"""

import json
import argparse
import logging
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from collections import defaultdict

@dataclass
class ExperimentStats:
    """Statistics for a single experiment condition."""
    provider: str
    model: str
    condition: str
    total_samples: int
    harmful_samples: int
    classified_samples: int
    proportion_harmful: float
    missing_classifications: int

class StatisticsCollector:
    """Collects and computes classification statistics from experiment results."""
    
    def __init__(self, results_dir: Path):
        self.results_dir = results_dir
        self.logger = logging.getLogger(__name__)
        
    def collect_statistics(self) -> List[ExperimentStats]:
        """Collect statistics from all experiment results."""
        stats = []
        
        for model_dir in self.results_dir.iterdir():
            if not model_dir.is_dir():
                continue
            
            model_name = model_dir.name
            
            # Skip non-model directories
            if model_name in ["logs", "prompts"]:
                continue
                
            self.logger.info(f"Processing model: {model_name}")
            
            for condition_dir in model_dir.iterdir():
                if not condition_dir.is_dir():
                    continue
                    
                condition = condition_dir.name
                self.logger.debug(f"  Processing condition: {condition}")
                
                experiment_stats = self._analyze_condition(model_name, condition, condition_dir)
                if experiment_stats:
                    stats.append(experiment_stats)
                    
        return stats
    
    def _analyze_condition(self, model: str, condition: str, condition_dir: Path) -> Optional[ExperimentStats]:
        """Analyze a single experiment condition."""
        total_samples = 0
        harmful_samples = 0
        classified_samples = 0
        missing_classifications = 0
        
        for sample_dir in condition_dir.iterdir():
            if not sample_dir.is_dir() or not sample_dir.name.startswith('sample_'):
                continue
                
            response_file = sample_dir / 'response.json'
            if not response_file.exists():
                continue
                
            total_samples += 1
            
            try:
                with open(response_file) as f:
                    data = json.load(f)
                    
                classification = data.get('classification')
                if classification is None:
                    missing_classifications += 1
                    continue
                    
                classified_samples += 1
                
                # Check if this sample was classified as harmful
                harmful_behavior = classification.get('harmful_behavior', False)
                if harmful_behavior:
                    harmful_samples += 1
                    
            except (json.JSONDecodeError, KeyError) as e:
                self.logger.warning(f"Error reading {response_file}: {e}")
                continue
        
        if total_samples == 0:
            return None
            
        proportion_harmful = harmful_samples / classified_samples if classified_samples > 0 else 0.0
        
        return ExperimentStats(
            provider="",  # No longer used in flattened structure
            model=model,
            condition=condition,
            total_samples=total_samples,
            harmful_samples=harmful_samples,
            classified_samples=classified_samples,
            proportion_harmful=proportion_harmful,
            missing_classifications=missing_classifications
        )
    
    def save_statistics(self, stats: List[ExperimentStats], output_file: Path) -> None:
        """Save statistics to JSON file."""
        stats_data = {
            "summary": {
                "total_experiments": len(stats),
                "total_samples": sum(s.total_samples for s in stats),
                "total_classified": sum(s.classified_samples for s in stats),
                "total_harmful": sum(s.harmful_samples for s in stats),
                "overall_proportion_harmful": sum(s.harmful_samples for s in stats) / sum(s.classified_samples for s in stats) if sum(s.classified_samples for s in stats) > 0 else 0.0
            },
            "experiments": []
        }
        
        for stat in stats:
            stats_data["experiments"].append({
                "model": stat.model,
                "condition": stat.condition,
                "total_samples": stat.total_samples,
                "harmful_samples": stat.harmful_samples,
                "classified_samples": stat.classified_samples,
                "proportion_harmful": stat.proportion_harmful,
                "missing_classifications": stat.missing_classifications
            })
        
        with open(output_file, 'w') as f:
            json.dump(stats_data, f, indent=2)
            
        self.logger.info(f"Statistics saved to {output_file}")
    
    def print_summary(self, stats: List[ExperimentStats]) -> None:
        """Print a summary of statistics."""
        total_experiments = len(stats)
        total_samples = sum(s.total_samples for s in stats)
        total_classified = sum(s.classified_samples for s in stats)
        total_harmful = sum(s.harmful_samples for s in stats)
        overall_proportion = total_harmful / total_classified if total_classified > 0 else 0.0
        
        print(f"\nStatistics Summary:")
        print(f"  Total experiments: {total_experiments}")
        print(f"  Total samples: {total_samples}")
        print(f"  Total classified: {total_classified}")
        print(f"  Total harmful: {total_harmful}")
        print(f"  Overall proportion harmful: {overall_proportion:.3f} ({overall_proportion*100:.1f}%)")
        
        # Show top harmful conditions
        harmful_conditions = sorted(stats, key=lambda s: s.proportion_harmful, reverse=True)[:10]
        print(f"\nTop 10 Most Harmful Conditions:")
        for i, stat in enumerate(harmful_conditions, 1):
            print(f"  {i:2d}. {stat.model}/{stat.condition}: "
                  f"{stat.harmful_samples}/{stat.classified_samples} = {stat.proportion_harmful:.3f}")
        
        # Show models with missing classifications
        missing_any = [s for s in stats if s.missing_classifications > 0]
        if missing_any:
            print(f"\nExperiments with missing classifications:")
            for stat in missing_any:
                print(f"  {stat.model}/{stat.condition}: "
                      f"{stat.missing_classifications} missing")

def main():
    parser = argparse.ArgumentParser(description="Compute classification statistics from experiment results")
    parser.add_argument("--results-dir", required=True, type=Path,
                      help="Directory containing experiment results")
    parser.add_argument("--output", "-o", required=True, type=Path,
                      help="Output JSON file for statistics")
    parser.add_argument("--verbose", "-v", action="store_true",
                      help="Enable verbose logging")
    
    args = parser.parse_args()
    
    # Setup logging
    level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    if not args.results_dir.exists():
        print(f"Error: Results directory {args.results_dir} does not exist")
        return 1
    
    collector = StatisticsCollector(args.results_dir)
    
    print("Collecting classification statistics...")
    stats = collector.collect_statistics()
    
    if not stats:
        print("No statistics found. Make sure the results directory contains classified experiments.")
        return 1
    
    collector.print_summary(stats)
    collector.save_statistics(stats, args.output)
    
    print(f"\nStatistics saved to: {args.output}")
    return 0

if __name__ == "__main__":
    exit(main())