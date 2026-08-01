"""Tests for package and MCP runtime version synchronization."""

from importlib import metadata

from mcp.server.lowlevel import NotificationOptions

from lunar_mcp_server import __version__
from lunar_mcp_server import _version as version_module
from lunar_mcp_server.server import LunarMCPServer


def test_package_version_matches_installed_distribution() -> None:
    """The public runtime version must come from installed package metadata."""
    assert __version__ == metadata.version(version_module.DISTRIBUTION_NAME)


def test_mcp_initialization_reports_package_version() -> None:
    """MCP initialization metadata must expose the installed package version."""
    server = LunarMCPServer().server
    options = server.create_initialization_options(
        notification_options=NotificationOptions()
    )

    assert server.version == __version__
    assert options.server_version == __version__


def test_source_tree_fallback_is_deterministic(monkeypatch) -> None:
    """Source execution without distribution metadata uses a stable fallback."""

    def missing_distribution(_: str) -> str:
        raise metadata.PackageNotFoundError

    monkeypatch.setattr(version_module.metadata, "version", missing_distribution)

    assert version_module.resolve_version() == version_module.SOURCE_TREE_VERSION
    assert version_module.SOURCE_TREE_VERSION == "0+unknown"
