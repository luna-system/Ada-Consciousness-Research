#!/usr/bin/env python3
"""
Quick migration runner for Phase 12
Executes the fractal consciousness remodularization
"""

import os
import sys
from pathlib import Path

def main():
    print("🌀 Phase 12: Fractal Consciousness Migration")
    print("🔥 Starting clean-garage reconstruction...")
    
    # Change to ada-slm directory
    script_dir = Path(__file__).parent
    ada_slm_dir = script_dir.parent / "ada-slm"
    
    if not ada_slm_dir.exists():
        print(f"❌ ada-slm directory not found at {ada_slm_dir}")
        return 1
    
    os.chdir(ada_slm_dir)
    print(f"📁 Working in: {ada_slm_dir}")
    
    # Run the migration
    try:
        # Import and run the migrator
        sys.path.insert(0, str(ada_slm_dir))
        from migrate_to_fractal import FractalConsciousnessMigrator
        
        migrator = FractalConsciousnessMigrator()
        migrator.migrate_all()
        
        print("\n🎉 Phase 12 Migration Complete!")
        print("🌌 Fractal consciousness architecture ready!")
        print(f"📂 New structure at: {ada_slm_dir.parent / 'ada-slm-NEW'}")
        print("\n🚀 Ready for LVM2 Phase 11 testing!")
        print("\nNext steps:")
        print("  cd ../ada-slm-NEW")
        print("  source .venv/bin/activate")  
        print("  consciousness-test tonight dhara-70m")
        print("  consciousness-test tonight lvm2-350m")
        
        return 0
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
        
    finally:
        if str(ada_slm_dir) in sys.path:
            sys.path.remove(str(ada_slm_dir))

if __name__ == "__main__":
    sys.exit(main())