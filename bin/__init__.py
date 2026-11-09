"""
Meet AI Agents - Enterprise Multi-Agent System & Automation Engine.

Created by Meet Uddeshi.
"""

__version__ = "1.0.0"
__author__ = "Meet Uddeshi"

try:
    from bin.installer import Installer
    from bin.mcp_manager import McpManager
    from bin.memory_manager import MemoryManager
except ImportError:
    from .installer import Installer
    from .mcp_manager import McpManager
    from .memory_manager import MemoryManager

__all__ = ["__version__", "__author__", "Installer", "McpManager", "MemoryManager"]

