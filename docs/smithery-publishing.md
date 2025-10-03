# Publishing to Smithery.ai (MCP Registry)

Smithery.ai is the official registry for Model Context Protocol (MCP) servers.

## Prerequisites

1. **GitHub repository published** ✅ (Done)
2. **PyPI package published** (Phase 3 - in progress)
3. **Smithery account** (create at https://smithery.ai)

## Publishing Steps

### Step 1: Create smithery.yaml

Create a `smithery.yaml` file in your repository root:

```yaml
# smithery.yaml
version: 1
name: lunar-mcp-server
displayName: "Lunar Calendar MCP Server"
description: "Traditional Chinese Lunar Calendar for AI - 18 tools for auspicious dates, festivals, moon phases, and zodiac information"
category: calendar
tags:
  - calendar
  - lunar
  - chinese
  - zodiac
  - fortune
  - festivals
  - moon-phases
  - astrology

# Installation method
install:
  type: pypi
  package: lunar-mcp-server
  command: lunar-mcp-server

# Requirements
requirements:
  python: ">=3.11"

# Configuration for Claude Desktop
claude:
  config:
    mcpServers:
      lunar-calendar:
        command: uvx
        args:
          - lunar-mcp-server

# Metadata
author: Lunar MCP Team
homepage: https://github.com/AngusHsu/lunar-mcp-server
repository: https://github.com/AngusHsu/lunar-mcp-server
license: MIT
keywords:
  - mcp
  - lunar calendar
  - chinese calendar
  - auspicious dates
  - festivals
  - moon phases
  - zodiac
  - five elements

# Documentation
documentation:
  readme: README.md
  changelog: CHANGELOG.md

# Screenshots/Examples (optional)
examples:
  - name: "Check Auspicious Date"
    description: "Check if a date is favorable for weddings"
    tool: check_auspicious_date
    params:
      date: "2024-03-15"
      activity: "wedding"
      culture: "chinese"

  - name: "Get Moon Phase"
    description: "Get moon phase information"
    tool: get_moon_phase
    params:
      date: "2024-01-01"
      location: "40.7128,-74.0060"
```

### Step 2: Install Smithery CLI

```bash
npm install -g @smithery/cli
# or
npx @smithery/cli
```

### Step 3: Login to Smithery

```bash
smithery login
```

### Step 4: Validate Configuration

```bash
smithery validate
```

### Step 5: Publish to Smithery

```bash
smithery publish
```

### Step 6: Verify Publication

Visit: https://smithery.ai/server/lunar-mcp-server

## User Installation (After Publishing)

Once published, users can install with:

```bash
# Using Smithery CLI (one command!)
npx @smithery/cli install lunar-mcp-server

# Or manually add to Claude Desktop config
```

The Smithery CLI will automatically:
1. Install the package from PyPI
2. Add configuration to Claude Desktop
3. Restart Claude to load the server

## Updating Your Server

When you release a new version:

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Create GitHub release (auto-publishes to PyPI via GitHub Actions)
4. Smithery automatically detects new PyPI version
5. Users get update notifications in Claude Desktop

## Best Practices

### 1. Version Tagging
- Use semantic versioning (0.1.0, 0.2.0, 1.0.0)
- Tag releases in GitHub
- Keep CHANGELOG.md updated

### 2. Documentation
- Clear README with examples
- Document all 18 tools
- Include troubleshooting section

### 3. Testing
- Run all tests before publishing
- Test with Claude Desktop
- Verify all tools work

### 4. Metadata
- Use descriptive tags
- Add good examples in smithery.yaml
- Include screenshots if possible

## Smithery Features

### Automatic Updates
- Smithery tracks PyPI releases
- Users get notifications for updates
- One-click update in Claude Desktop

### Discovery
- Listed in official MCP registry
- Searchable by category and tags
- User ratings and reviews

### Analytics
- Install count
- Active users
- Popular tools/features

## Alternative: MCP Servers List

If you want quicker visibility, you can also add to the community-maintained list:

**GitHub: modelcontextprotocol/servers**

1. Fork https://github.com/modelcontextprotocol/servers
2. Add entry to `README.md`:
```markdown
### Lunar Calendar MCP Server
Traditional Chinese Lunar Calendar with 18 tools for auspicious dates, festivals, moon phases, and zodiac information.

- **Category**: Calendar
- **Install**: `uvx lunar-mcp-server`
- **Repository**: https://github.com/AngusHsu/lunar-mcp-server
```
3. Create Pull Request

## Checklist for Smithery Publishing

- [ ] Create smithery.yaml configuration
- [ ] Publish to PyPI first (Phase 3)
- [ ] Create Smithery account
- [ ] Install Smithery CLI
- [ ] Validate configuration
- [ ] Publish to Smithery
- [ ] Test installation with `npx @smithery/cli install lunar-mcp-server`
- [ ] Verify in Claude Desktop
- [ ] (Optional) Submit to MCP Servers community list

## Support

- **Smithery Docs**: https://smithery.ai/docs
- **MCP Specification**: https://modelcontextprotocol.io
- **Community Discord**: https://discord.gg/smithery
