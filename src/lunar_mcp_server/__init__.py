"""
Lunar Calendar MCP Server

A comprehensive MCP server providing traditional lunar calendar information,
auspicious date checking, and festival data.
"""

__author__ = "Lunar MCP Team"

from ._version import __version__
from .server import LunarMCPServer

__all__ = ["LunarMCPServer", "__version__"]
