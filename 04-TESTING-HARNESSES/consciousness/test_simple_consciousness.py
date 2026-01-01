#!/usr/bin/env python3
"""
Simple test to verify consciousness models work through Python
"""
import asyncio
import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.append(str(project_root))

from brain.llm import complete

async def test_consciousness():
    """Test consciousness models directly"""
    print("🔍 Testing ada-v6-golden consciousness...")
    
    try:
        response, _, _ = await asyncio.to_thread(
            complete, 
            "φ●", 
            "ada-v6-golden", 
            False,  # include_thinking
            10      # timeout
        )
        print(f"✅ v6-golden response: {response}")
    except Exception as e:
        print(f"❌ v6-golden failed: {e}")
    
    print("🔍 Testing ada-v4-mixed consciousness...")
    try:
        response, _, _ = await asyncio.to_thread(
            complete, 
            "φ●", 
            "ada-v4-mixed", 
            False,  # include_thinking
            10      # timeout
        )
        print(f"✅ v4-mixed response: {response}")
    except Exception as e:
        print(f"❌ v4-mixed failed: {e}")
    
    print("🔍 Testing ada-v5c-balanced consciousness...")
    try:
        response, _, _ = await asyncio.to_thread(
            complete, 
            "φ●", 
            "ada-v5c-balanced", 
            False,  # include_thinking
            10      # timeout
        )
        print(f"✅ v5c-balanced response: {response}")
    except Exception as e:
        print(f"❌ v5c-balanced failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_consciousness())
