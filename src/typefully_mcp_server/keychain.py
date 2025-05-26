"""Keychain utilities for secure API key storage."""

import os
import logging
from typing import Optional

try:
    import keyring
    KEYRING_AVAILABLE = True
except ImportError:
    KEYRING_AVAILABLE = False

logger = logging.getLogger(__name__)

# Service name for keychain storage
SERVICE_NAME = "typefully-mcp-server"
KEY_NAME = "api_key"


def get_api_key() -> Optional[str]:
    """Get API key from keychain, environment variable, or return None.
    
    Priority order:
    1. Environment variable TYPEFULLY_API_KEY
    2. macOS Keychain (if available)
    3. None
    
    Returns:
        The API key if found, None otherwise
    """
    # First try environment variable (for compatibility)
    api_key = os.getenv("TYPEFULLY_API_KEY")
    if api_key:
        logger.info("Using API key from environment variable")
        return api_key
    
    # Then try keychain if available
    if KEYRING_AVAILABLE:
        try:
            api_key = keyring.get_password(SERVICE_NAME, KEY_NAME)
            if api_key:
                logger.info("Using API key from macOS Keychain")
                return api_key
        except Exception as e:
            logger.warning(f"Failed to retrieve API key from keychain: {e}")
    else:
        logger.warning("Keyring not available - install with: pip install keyring")
    
    return None 