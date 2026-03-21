#!/usr/bin/env python3
"""
build_docs.py — Auto-generates markdown wrappers for code files,
then builds the MkDocs site.

Usage:
    python3 build_docs.py          # or .venv/bin/python build_docs.py

What it does:
1. Scans all code/ folders for .py and .ipynb files
2. For .py files: creates _generated/{name}.md with embedded code
3. Auto-generates nav entries for mkdocs.yml
4. Runs mkdocs build
5. Touches docs/.nojekyll

Run this EVERY TIME after adding/updating notes or code.
"""

import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent
CONTENT = ROOT / "content"
GENERATED_DIR = "_generated"


def find_code_files(base_path: Path):
    """Find all .py files under code/ directories, following symlinks."""
    results = []
    for dirpath, dirnames, filenames in os.walk(base_path, followlinks=True):
        dirpath = Path(dirpath)
        # Only look inside code/ directories
        if "code" not in dirpath.parts:
            continue
        for f in filenames:
            if f.endswith(".py"):
                results.append(dirpath / f)
    return sorted(results)


def generate_py_wrapper(py_file: Path, content_root: Path):
    """Create a markdown file that embeds the Python code with syntax highlighting."""
    rel_path = py_file.relative_to(content_root)
    
    # Generate markdown in a _generated folder mirroring the structure
    gen_dir = content_root / GENERATED_DIR / rel_path.parent
    gen_dir.mkdir(parents=True, exist_ok=True)
    
    md_path = gen_dir / f"{py_file.stem}.md"
    
    # Read the Python source
    code = py_file.read_text(encoding="utf-8")
    
    # Extract docstring or first comment as description
    desc = ""
    if code.strip().startswith('"""'):
        match = re.search(r'"""(.*?)"""', code, re.DOTALL)
        if match:
            desc = match.group(1).strip().split('\n')[0]
    elif code.strip().startswith('#'):
        first_line = code.strip().split('\n')[0]
        desc = first_line.lstrip('# ').strip()
    
    # Build markdown
    title = py_file.stem.replace('_', ' ').title()
    
    md_content = f"""# 📄 {title}

**File:** `{rel_path}`
{f'> {desc}' if desc else ''}

```python
{code}
```

---

> [⬇️ Download raw file](/{rel_path})
"""
    
    md_path.write_text(md_content, encoding="utf-8")
    return md_path.relative_to(content_root)


def update_mkdocs_nav(content_root: Path):
    """Read mkdocs.yml, find code sections, update with generated files."""
    mkdocs_path = ROOT / "mkdocs.yml"
    config = mkdocs_path.read_text(encoding="utf-8")
    
    # Find all generated .md files
    gen_dir = content_root / GENERATED_DIR
    if not gen_dir.exists():
        return
    
    generated_files = sorted(gen_dir.rglob("*.md"))
    
    # Build nav entries grouped by topic
    nav_entries = {}
    for gf in generated_files:
        rel = gf.relative_to(content_root)
        # Group by the code's parent topic path
        parts = list(rel.parts)
        # _generated/tech/python/asyncio/code/L1/example_1.md
        # → topic key: tech/python/asyncio
        if GENERATED_DIR in parts:
            parts.remove(GENERATED_DIR)
        
        # Find the "code" part to split topic from file
        if "code" in parts:
            code_idx = parts.index("code")
            topic_key = "/".join(parts[:code_idx])
            file_name = parts[-1].replace('.md', '')
            title = file_name.replace('_', ' ').title()
            
            if topic_key not in nav_entries:
                nav_entries[topic_key] = []
            nav_entries[topic_key].append((title, str(rel)))
    
    return nav_entries


def build_full_nav():
    """Generate the complete nav section for mkdocs.yml."""
    content_root = CONTENT
    
    # Generate wrappers for all .py files
    py_files = find_code_files(content_root)
    generated = []
    for pf in py_files:
        gen_path = generate_py_wrapper(pf, content_root)
        generated.append(gen_path)
        print(f"  📄 Generated: {gen_path}")
    
    return generated


def main():
    print("🔧 Building My Memory docs...\n")
    
    # Ensure content symlinks exist
    content_dir = ROOT / "content"
    content_dir.mkdir(exist_ok=True)
    
    for item in ["README.md", "tech", "_maps", "_revision", "_assets"]:
        link = content_dir / item
        target = Path("..") / item
        if not link.exists():
            link.symlink_to(target)
            print(f"  🔗 Symlinked: content/{item}")
    
    # Generate .py wrappers
    print("\n📝 Generating code wrappers...")
    generated = build_full_nav()
    print(f"  ✅ Generated {len(generated)} code pages\n")
    
    # Symlink _generated into content
    gen_source = ROOT / "content" / GENERATED_DIR
    gen_target = ROOT / GENERATED_DIR
    if not gen_target.exists():
        gen_target.symlink_to(gen_source)
    
    # Build mkdocs
    print("🏗️  Running mkdocs build...")
    result = subprocess.run(
        [str(ROOT / ".venv" / "bin" / "mkdocs"), "build"],
        cwd=str(ROOT),
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print(f"❌ Build failed:\n{result.stderr}")
        sys.exit(1)
    
    # Add .nojekyll
    (ROOT / "docs" / ".nojekyll").touch()
    
    print("✅ Build complete!")
    print(f"📂 Output: {ROOT / 'docs'}")
    print(f"📄 Pages: {len(list((ROOT / 'docs').rglob('index.html')))}")
    print("\n🚀 Ready to commit & push!")


if __name__ == "__main__":
    main()
