"""Runtime package version resolution."""

from importlib import metadata

DISTRIBUTION_NAME = "lunar-mcp-server"
SOURCE_TREE_VERSION = "0+unknown"


def resolve_version() -> str:
    """Return installed distribution metadata or a deterministic source fallback."""
    try:
        return metadata.version(DISTRIBUTION_NAME)
    except metadata.PackageNotFoundError:
        return SOURCE_TREE_VERSION


__version__ = resolve_version()
