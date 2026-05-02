# Claude Skills

This directory contains all available Claude skills, including official Anthropic skills and custom project-specific skills.

**Source**: Cloned from [anthropics/skills](https://github.com/anthropics/skills) repository  
**Last Updated**: 2026-04-23

---

## Available Skills

### 🔍 Code Review & Quality

#### `full-review/` ⭐ (Custom)
**Purpose**: Launch all code review agents in parallel  
**Use when**: Before creating a PR, after completing a feature  
**Speed**: ~2-3 minutes (parallel execution)  
**Coverage**: 8 specialized agents analyzing changed files only

**Example**: `/full-review`

---

### 🛠️ Development & Testing

#### `webapp-testing/`
**Purpose**: Test local web applications using Playwright  
**Features**: Browser automation, screenshot capture, log inspection  
**Example**: "Test the login flow on localhost:3000"

#### `claude-api/`
**Purpose**: Build LLM applications with Claude API  
**Features**: Model selection, tool use, streaming, structured outputs  
**Example**: "Create an API client for text classification"

#### `mcp-builder/`
**Purpose**: Build Model Context Protocol (MCP) servers  
**Features**: Protocol scaffolding, tool integration  
**Example**: "Build an MCP server for our wiki"

#### `skill-creator/`
**Purpose**: Build and test custom skills  
**Features**: Scaffolding, evaluation framework, iteration workflow  
**Example**: "Create a skill for performance testing"

---

### 📄 Document Processing

#### `pdf/`
**Purpose**: Extract and manipulate PDF documents  
**Example**: "Extract tables from this PDF report"

#### `docx/`
**Purpose**: Create and edit Word documents  
**Example**: "Generate a requirements doc from these specs"

#### `pptx/`
**Purpose**: Create and edit PowerPoint presentations  
**Example**: "Create a slide deck from this markdown"

#### `xlsx/`
**Purpose**: Create and edit Excel spreadsheets  
**Example**: "Export user data to Excel with formatting"

---

### 🎨 Design & Creative

#### `canvas-design/`
**Purpose**: Design canvas-based interfaces and layouts  
**Example**: "Design a dashboard layout"

#### `frontend-design/`
**Purpose**: Frontend design techniques and patterns  
**Example**: "Design a responsive navigation component"

#### `algorithmic-art/`
**Purpose**: Generate algorithmic art and visualizations  
**Example**: "Create a fractal visualization"

#### `theme-factory/`
**Purpose**: Generate and customize UI themes  
**Example**: "Create a dark mode theme"

#### `web-artifacts-builder/`
**Purpose**: Build web artifacts and components  
**Example**: "Create an interactive chart component"

---

### 💬 Communication & Content

#### `doc-coauthoring/`
**Purpose**: Collaborative document creation  
**Example**: "Co-author a technical spec"

#### `internal-comms/`
**Purpose**: Internal communications and announcements  
**Example**: "Draft a team update email"

#### `slack-gif-creator/`
**Purpose**: Create GIFs for Slack  
**Example**: "Create a celebration GIF"

#### `brand-guidelines/`
**Purpose**: Brand identity and guidelines  
**Example**: "Generate brand voice guidelines"

---

## How to Use Skills

### Invoke a Skill
```bash
/skill-name [arguments]
```

### Examples
```bash
# Full code review (custom)
/full-review

# Test web application
/webapp-testing

# Create Excel report
/xlsx

# Build MCP server
/mcp-builder

# Create new skill
/skill-creator
```

---

## Skill Structure

Skills follow the [Agent Skills specification](http://agentskills.io):

```
skill-name/
├── SKILL.md              # Main skill instructions (required)
├── scripts/              # Helper scripts (optional)
├── examples/             # Example usage (optional)
└── resources/            # Additional assets (optional)
```

**SKILL.md frontmatter**:
```markdown
---
name: skill-name
description: Clear description of what it does and when to use it
---

# Instructions
...
```

---

## Creating Custom Skills

Use `/skill-creator` to build project-specific skills:

1. **Define intent** - What should the skill do?
2. **Draft SKILL.md** - Write instructions with metadata
3. **Create test cases** - 2-3 realistic prompts
4. **Run evaluations** - Test with/without skill
5. **Iterate** - Improve based on results

### Best Practices

**Progressive Disclosure**:
- **Metadata** (name + description): Always loaded
- **SKILL.md body**: Loaded when triggered (~500 lines max)
- **Bundled resources**: Scripts and assets as needed

**Clear Instructions**:
- Explain the "why" behind steps
- Use concrete examples
- Remove anything not pulling weight
- Generalize from feedback

**Testing**:
- Create realistic test prompts
- Compare outputs with/without skill
- Iterate based on results

---

## Project-Specific Skills

### `full-review/` - Comprehensive Code Review

**What it does**:
- Launches 8 specialized review agents in parallel
- Analyzes only changed files (git diff)
- Returns unified report with all findings
- Based on real project bug patterns

**Agents launched**:
1. **branch-code-reviewer** - Overall quality, bugs, test gaps
2. **logic-correctness-reviewer** - Off-by-one, edge cases
3. **performance-reviewer** - N+1 queries, async optimization
4. **security-reviewer** - Cross-tenant, SQL injection, XSS
5. **db-ops-reviewer** - Database efficiency
6. **resource-leak-detector** - Unclosed resources
7. **test-quality-reviewer** - Mock targets, assertions

**When to use**:
- Before creating a PR
- After completing a feature
- For large changes (10+ files)
- When you want fast comprehensive analysis

**Advantages over single reviewer**:
- **3x faster** (2-3 min vs 5-8 min)
- **More detailed** (8 specialized agents)
- **Parallel execution** (no waiting)

---

## Skill Catalog

| Skill | Category | Purpose | Status |
|-------|----------|---------|--------|
| `full-review` | Code Review | Parallel agent review | ⭐ Custom |
| `webapp-testing` | Development | Playwright testing | Official |
| `claude-api` | Development | Claude API integration | Official |
| `mcp-builder` | Development | MCP server builder | Official |
| `skill-creator` | Development | Build custom skills | Official |
| `pdf` | Documents | PDF handling | Official |
| `docx` | Documents | Word documents | Official |
| `pptx` | Documents | PowerPoint | Official |
| `xlsx` | Documents | Excel spreadsheets | Official |
| `canvas-design` | Design | Canvas layouts | Official |
| `frontend-design` | Design | Frontend patterns | Official |
| `algorithmic-art` | Design | Generative art | Official |
| `theme-factory` | Design | UI themes | Official |
| `web-artifacts-builder` | Design | Web components | Official |
| `doc-coauthoring` | Communication | Collaborative docs | Official |
| `internal-comms` | Communication | Team comms | Official |
| `slack-gif-creator` | Communication | Slack GIFs | Official |
| `brand-guidelines` | Branding | Brand identity | Official |

---

## Related Resources

- **Agent Skills Spec**: [agentskills.io](http://agentskills.io)
- **Official Repository**: [anthropics/skills](https://github.com/anthropics/skills)
- **Project Bug Patterns**: `../.claude/agents/PROJECT-BUG-PATTERNS.md`
- **Review Agents**: `../.claude/agents/`

---

## Quick Start Examples

### Code Review Before PR
```bash
# Make changes
git add .
git commit -m "feat: add feature"

# Full review
/full-review

# Fix issues, create PR
gh pr create
```

### Test Web Application
```bash
# Start your server
npm run dev

# Test in browser
/webapp-testing
```

### Generate Excel Report
```bash
# Process data and export
/xlsx
```

### Build Custom Skill
```bash
# Create new skill
/skill-creator

# Follow prompts to build, test, iterate
```

---

**🎉 All Skills Ready!**

Type `/skill-name` to invoke any skill, or `/full-review` for comprehensive parallel code review!
