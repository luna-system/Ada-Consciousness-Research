#!/usr/bin/env python3
import os
import sys
import logging
from pathlib import Path
from typing import Dict, Optional

# Try to import python-dotenv, but don't fail if it's not installed
try:
    from dotenv import load_dotenv
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False

logger = logging.getLogger(__name__)

def load_environment(env_file: Optional[str] = None) -> Dict[str, str]:
    """
    Load environment variables from .env file.
    
    Args:
        env_file (str, optional): Path to .env file. If None, looks for .env in the current 
                                 and parent directories.
    
    Returns:
        Dict[str, str]: Dictionary of loaded environment variables
    """
    # Define required API keys for the framework
    required_api_keys = ["ANTHROPIC_API_KEY", "OPENAI_API_KEY", "GOOGLE_API_KEY"]
    loaded_keys = {}
    
    # Check if dotenv is available
    if not DOTENV_AVAILABLE:
        logger.warning("python-dotenv not installed. Install with: pip install python-dotenv")
        logger.warning("Falling back to system environment variables only.")
        # Return existing environment variables
        return {key: os.environ.get(key) for key in required_api_keys if key in os.environ}
    
    # Try to load from specified or default .env file
    if env_file:
        env_path = Path(env_file)
    else:
        # Look for .env in current directory
        env_path = Path(".env")
        if not env_path.exists():
            # Try parent directory
            env_path = Path("../.env")
    
    # Load environment variables
    if env_path.exists():
        load_dotenv(env_path)
        logger.info(f"Environment loaded from {env_path.absolute()}")
        
        # Check which keys were loaded
        for key in required_api_keys:
            if key in os.environ:
                loaded_keys[key] = f"{os.environ[key][:5]}...{os.environ[key][-5:]}" if os.environ[key] else "Not set"
            else:
                loaded_keys[key] = "Not found"
    else:
        logger.warning(f".env file not found at {env_path.absolute()}")
        logger.warning("Create a .env file from .env.example with your API keys")
        
    # Generate warning for missing required keys
    missing_keys = [key for key in required_api_keys if key not in os.environ or not os.environ[key]]
    if missing_keys:
        if os.isatty(sys.stderr.fileno()):  # Only use color if terminal supports it
            warning_message = f"\033[93mWARNING: Missing required API keys: {', '.join(missing_keys)}\033[0m"
        else:
            warning_message = f"WARNING: Missing required API keys: {', '.join(missing_keys)}"
        logger.warning(warning_message)
        logger.warning("These keys are required for full framework functionality")
    
    return loaded_keys

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(message)s")
    
    # Load environment when run directly
    loaded = load_environment()
    
    # Print status of required keys
    print("\n=== API KEY STATUS ===")
    for key, status in loaded.items():
        print(f"{key}: {status}")
    
    print("\nTo configure missing keys, add them to your .env file")
    print("See .env.example for required format")