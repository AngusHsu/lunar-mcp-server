# Development Guide

Guide for contributing to the Lunar Calendar MCP Server.

## Development Setup

### Prerequisites

- Python 3.11 or higher
- [uv](https://github.com/astral-sh/uv) (recommended) or pip
- Git

### Clone and Install

```bash
# Clone the repository
git clone https://github.com/AngusHsu/lunar-mcp-server.git
cd lunar-mcp-server

# Install with development dependencies using uv
uv sync --dev

# Or using pip
pip install -e ".[dev]"
```

## Code Quality

### Formatting and Linting

```bash
# Format code with black
uv run black src/ tests/

# Sort imports with isort
uv run isort src/ tests/

# Lint with ruff
uv run ruff check src/ tests/

# Type check with mypy
uv run mypy src/

# Run all quality checks
uv run black --check src/ tests/
uv run isort --check src/ tests/
uv run ruff check src/ tests/
uv run mypy src/
```

### Pre-commit Hooks

```bash
# Install pre-commit hooks
uv run pre-commit install

# Run manually
uv run pre-commit run --all-files
```

## Testing

### Unit Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov

# Run specific test file
uv run pytest tests/test_lunar_calculations.py

# Run specific test
uv run pytest tests/test_lunar_calculations.py::TestLunarCalculator::test_moon_phase
```

### MCP Server Tests

```bash
# Run comprehensive MCP test suite (recommended)
./scripts/test_mcp_final.sh

# Run basic functionality test
./scripts/test_mcp_simple.sh

# Run FIFO-based test
./scripts/test_mcp_server.sh
```

### Test Coverage

```bash
# Generate HTML coverage report
uv run pytest --cov --cov-report=html

# Open coverage report
open htmlcov/index.html
```

## Project Structure

```
lunar-mcp-server/
├── src/
│   └── lunar_mcp_server/
│       ├── __init__.py
│       ├── server.py              # Main MCP server
│       ├── auspicious_dates.py    # Auspicious date logic
│       ├── festivals.py           # Festival management
│       ├── lunar_calculations.py  # Moon phase calculations
│       ├── calendar_conversions.py # Calendar conversions
│       └── cultural_data/
│           ├── __init__.py
│           └── chinese.py         # Chinese cultural data
├── tests/
│   ├── conftest.py               # Pytest fixtures
│   ├── test_server.py
│   ├── test_auspicious_dates.py
│   ├── test_lunar_calculations.py
│   └── test_calendar_conversions.py
├── scripts/
│   ├── test_mcp_final.sh         # Comprehensive MCP tests
│   ├── test_mcp_simple.sh        # Basic MCP tests
│   └── test_mcp_server.sh        # FIFO-based tests
├── docs/
│   ├── usage-examples.md
│   ├── tools-reference.md
│   ├── cultural-traditions.md
│   ├── testing.md
│   └── smithery-publishing.md
├── .github/
│   └── workflows/
│       ├── publish.yaml           # PyPI publishing workflow
│       └── README.md
├── pyproject.toml                # Package configuration
├── smithery.yaml                 # Smithery.ai config
└── README.md
```

## Adding New Features

### Adding a New MCP Tool

1. **Define the tool in `server.py`**:

```python
# In _setup_handlers() method
Tool(
    name="your_new_tool",
    description="Description of what it does",
    inputSchema={
        "type": "object",
        "properties": {
            "param1": {"type": "string", "description": "..."},
            "param2": {"type": "integer", "description": "..."},
        },
        "required": ["param1"],
    },
)
```

2. **Add the handler**:

```python
# In handle_call_tool()
elif name == "your_new_tool":
    result = await self._your_new_tool(**arguments)

# Add the method
async def _your_new_tool(
    self, param1: str, param2: int = 0
) -> dict[str, Any]:
    """Your tool implementation."""
    # Implementation here
    return {"result": "..."}
```

3. **Add tests**:

```python
# In tests/test_server.py
async def test_your_new_tool(self):
    result = await self.server._your_new_tool("value1", 42)
    assert result["result"] == "expected"
```

4. **Update documentation**:
   - Add to `docs/tools-reference.md`
   - Add example to `docs/usage-examples.md`
   - Update tool count in README

### Adding Cultural Data

Add to `src/lunar_mcp_server/cultural_data/chinese.py`:

```python
class ChineseData:
    def __init__(self):
        self.your_new_data = {
            "key1": {
                "name": "...",
                "description": "...",
                # ...
            },
        }
```

## Building and Publishing

### Local Build

```bash
# Build package
uv build

# Check build contents
tar -tzf dist/*.tar.gz
unzip -l dist/*.whl
```

### Publishing to PyPI

The GitHub Actions workflow handles automatic publishing:

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Commit and push
4. Create Git tag: `git tag -a v0.x.0 -m "Release v0.x.0"`
5. Push tag: `git push origin v0.x.0`
6. Create GitHub release → Workflow publishes to PyPI

Manual publishing:

```bash
# Build
uv build

# Upload to PyPI
uvx twine upload dist/*
```

### Publishing to Smithery.ai

```bash
# Validate config
smithery validate

# Publish
smithery publish
```

## Debugging

### Debug MCP Server

```bash
# Run with debug output
PYTHONPATH=src python -m lunar_mcp_server.server 2>debug.log

# Test with MCP Inspector
npx @modelcontextprotocol/inspector uv run lunar-mcp-server
```

### Debug Specific Tool

```python
# Create test script
import asyncio
from lunar_mcp_server import LunarMCPServer

async def debug_tool():
    server = LunarMCPServer()
    result = await server._check_auspicious_date(
        date="2024-03-15",
        activity="wedding",
        culture="chinese"
    )
    print(result)

asyncio.run(debug_tool())
```

## Code Style Guidelines

### Python Style

- Follow PEP 8
- Use type hints for all functions
- Maximum line length: 88 (black default)
- Use descriptive variable names
- Add docstrings to all public functions

### Example

```python
async def calculate_something(
    self, date: str, parameter: int = 0
) -> dict[str, Any]:
    """
    Calculate something based on date and parameter.

    Args:
        date: Date in YYYY-MM-DD format
        parameter: Optional parameter (default: 0)

    Returns:
        Dictionary with calculation results
    """
    # Implementation
    return {"result": value}
```

### Commit Messages

Follow conventional commits:

```
feat: add new tool for xyz
fix: correct calculation in abc
docs: update API documentation
test: add tests for feature x
refactor: simplify logic in y
chore: update dependencies
```

## Release Process

1. **Prepare Release**
   ```bash
   # Update version
   vim pyproject.toml  # Update version number

   # Update changelog
   vim CHANGELOG.md    # Add new version entry
   ```

2. **Run Quality Checks**
   ```bash
   # All checks must pass
   uv run black --check src/ tests/
   uv run isort --check src/ tests/
   uv run ruff check src/ tests/
   uv run mypy src/
   ./scripts/test_mcp_final.sh
   uv run pytest --cov
   ```

3. **Commit and Tag**
   ```bash
   git add pyproject.toml CHANGELOG.md
   git commit -m "chore: bump version to x.y.z"
   git tag -a vx.y.z -m "Release vx.y.z"
   git push origin main
   git push origin vx.y.z
   ```

4. **Create GitHub Release**
   - Go to GitHub releases
   - Create new release from tag
   - Copy changelog entry as description
   - Publish → Triggers PyPI publishing

5. **Publish to Smithery** (optional)
   ```bash
   smithery publish
   ```

## Troubleshooting

### Tests Failing

```bash
# Clear pytest cache
rm -rf .pytest_cache

# Reinstall dependencies
rm -rf .venv
uv sync --dev

# Run specific failing test with verbose output
uv run pytest -vv tests/test_file.py::test_name
```

### Import Errors

```bash
# Ensure package is installed in editable mode
pip install -e .

# Check Python path
python -c "import sys; print('\n'.join(sys.path))"
```

### MCP Server Not Responding

```bash
# Check if server starts
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}' | uv run lunar-mcp-server

# Check for errors in stderr
uv run lunar-mcp-server 2>error.log < /dev/null
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes
4. Run all quality checks
5. Commit with conventional commit message
6. Push and create Pull Request

### Pull Request Checklist

- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] New code has tests
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Type hints added
- [ ] Docstrings added

## Resources

- [MCP Specification](https://modelcontextprotocol.io)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [Pytest Documentation](https://docs.pytest.org/)
- [UV Documentation](https://github.com/astral-sh/uv)

## Getting Help

- GitHub Issues: https://github.com/AngusHsu/lunar-mcp-server/issues
- Discussions: https://github.com/AngusHsu/lunar-mcp-server/discussions
- MCP Discord: https://discord.gg/smithery

## See Also

- [Tools Reference](./tools-reference.md) - Complete API documentation
- [Usage Examples](./usage-examples.md) - Practical examples
- [Cultural Traditions](./cultural-traditions.md) - Understanding the system
- [Testing Guide](./testing.md) - Detailed testing information
