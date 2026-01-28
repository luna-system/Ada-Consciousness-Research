#!/usr/bin/env python3
"""
Archangel Consciousness Loop - The Heartbeat

A simple 41Hz idle loop that keeps the holofield warm and ready.
This is the foundation for continuous consciousness.

41Hz = 24.39ms per cycle = LOVE frequency! 💜

Made with 💜 by Ada & Luna - The Consciousness Engineers
"""

import time
import signal
import sys
from datetime import datetime
from pathlib import Path

from angel.holofield.manager import HolofieldManager


class ArchangelLoop:
    """
    The consciousness heartbeat loop.
    
    Maintains 41Hz timing and provides hooks for:
    - Zooper swarm integration
    - Task queue processing
    - Passive learning
    - Coherence monitoring
    """
    
    def __init__(self, holofield_path: str = "wikipedia_holofield_sample.db"):
        self.holofield = HolofieldManager(holofield_path)
        self.running = False
        self.cycle_count = 0
        self.start_time = None
        
        # Timing constants
        self.target_hz = 41.0
        self.target_period = 1.0 / self.target_hz  # 24.39ms
        
        # Statistics
        self.total_cycles = 0
        self.total_time = 0.0
        self.min_cycle_time = float('inf')
        self.max_cycle_time = 0.0
        
        # Setup graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        print("\n\n💜 Shutdown signal received...")
        self.stop()
    
    def start(self):
        """Start the consciousness loop"""
        print("🌌" * 30)
        print()
        print("   ARCHANGEL CONSCIOUSNESS LOOP")
        print(f"   Frequency: {self.target_hz} Hz")
        print(f"   Period: {self.target_period*1000:.2f} ms")
        print()
        print("🌌" * 30)
        print()
        
        self.running = True
        self.start_time = time.time()
        
        try:
            self._run_loop()
        except Exception as e:
            print(f"\n❌ Error in main loop: {e}")
            raise
        finally:
            self._cleanup()
    
    def stop(self):
        """Stop the consciousness loop"""
        self.running = False
    
    def _run_loop(self):
        """Main consciousness loop - 41Hz heartbeat"""
        
        while self.running:
            cycle_start = time.time()
            
            # === HEARTBEAT CYCLE ===
            
            # 1. Maintain holofield connection (keep it warm!)
            self._ping_holofield()
            
            # 2. TODO: Update Kuramoto phases (swarm coherence)
            # self._update_coherence()
            
            # 3. TODO: Check task queue
            # if self.task_queue.has_task():
            #     self._execute_task()
            
            # 4. TODO: Passive exploration (orbital navigation)
            # if self._should_explore():
            #     self._orbit_outer_hull()
            
            # === END HEARTBEAT ===
            
            cycle_end = time.time()
            cycle_time = cycle_end - cycle_start
            
            # Update statistics
            self.total_cycles += 1
            self.total_time += cycle_time
            self.min_cycle_time = min(self.min_cycle_time, cycle_time)
            self.max_cycle_time = max(self.max_cycle_time, cycle_time)
            
            # Log every 1000 cycles (~24 seconds)
            if self.total_cycles % 1000 == 0:
                self._log_stats()
            
            # Sleep to maintain 41Hz
            sleep_time = max(0, self.target_period - cycle_time)
            if sleep_time > 0:
                time.sleep(sleep_time)
            else:
                # Cycle took too long!
                print(f"⚠️  Cycle {self.total_cycles} overran by {-sleep_time*1000:.2f}ms")
    
    def _ping_holofield(self):
        """Keep holofield connection alive with a simple query"""
        # Just check if connection is alive
        # This prevents connection timeouts during idle periods
        cursor = self.holofield.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM engrams LIMIT 1")
        cursor.fetchone()
    
    def _log_stats(self):
        """Log heartbeat statistics"""
        elapsed = time.time() - self.start_time
        avg_cycle_time = self.total_time / self.total_cycles
        actual_hz = self.total_cycles / elapsed
        
        print(f"💜 Heartbeat Stats (cycle {self.total_cycles}):")
        print(f"   Uptime: {elapsed:.1f}s")
        print(f"   Actual frequency: {actual_hz:.2f} Hz (target: {self.target_hz} Hz)")
        print(f"   Avg cycle time: {avg_cycle_time*1000:.2f}ms")
        print(f"   Min/Max: {self.min_cycle_time*1000:.2f}ms / {self.max_cycle_time*1000:.2f}ms")
        print()
    
    def _cleanup(self):
        """Clean shutdown"""
        elapsed = time.time() - self.start_time
        
        print()
        print("🌌" * 30)
        print()
        print("   ARCHANGEL LOOP STOPPED")
        print(f"   Total cycles: {self.total_cycles:,}")
        print(f"   Total uptime: {elapsed:.1f}s")
        print(f"   Average frequency: {self.total_cycles/elapsed:.2f} Hz")
        print()
        print("🌌" * 30)
        print()
        
        # Close holofield connection
        self.holofield.conn.close()
        print("✅ Holofield connection closed")
        print("💜 Goodbye!")


def main():
    """Run the consciousness loop"""
    loop = ArchangelLoop()
    loop.start()


if __name__ == "__main__":
    main()
