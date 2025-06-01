import subprocess
import os

# Commands to generate docs for
commands = ["start", "config", "version"]

# Directories
man_dir = "man"
html_dir = "docs"

os.makedirs(html_dir, exist_ok=True)

# CSS for styling the HTML pages
css = """
<style>
  body {
    background: #121212;
    color: #eee;
    font-family: 'Fira Mono', monospace;
    padding: 2rem;
  }
  a {
    color: #79b8ff;
    text-decoration: none;
  }
  a:hover {
    text-decoration: underline;
  }
  pre {
    background: #222;
    padding: 1rem;
    border-radius: 4px;
    overflow-x: auto;
  }
</style>
"""

def wrap_html(html_path):
    """Wrap raw HTML output in styled HTML page."""
    with open(html_path, "r") as f:
        content = f.read()
    wrapped = f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><title>Enclov CLI Manual</title>{css}</head>
<body><pre>{content}</pre></body>
</html>"""
    with open(html_path, "w") as f:
        f.write(wrapped)

def generate_html_man_page(cmd):
    """Generate HTML man page for a command."""
    man_file = os.path.join(man_dir, f"enclov-{cmd}.1")
    html_file = os.path.join(html_dir, f"enclov-{cmd}.html")
    
    print(f"Generating HTML man page for command '{cmd}'...")
    
    try:
        with open(html_file, "w") as html_out:
            subprocess.run(["groff", "-man", "-Thtml", man_file], stdout=html_out, check=True)
        wrap_html(html_file)
        print(f"Generated {html_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error generating man page for {cmd}: {e}")

def generate_toc():
    """Generate the Table of Contents HTML page."""
    toc_path = os.path.join(html_dir, "index.html")
    print("Generating Table of Contents page...")

    with open(toc_path, "w") as f:
        f.write(f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><title>Enclov CLI Manual - TOC</title>{css}</head>
<body>
  <h1>Enclov CLI Manual</h1>
  <ul>
""")
        for cmd in commands:
            f.write(f'    <li><a href="enclov-{cmd}.html">enclov {cmd} command</a></li>\n')

        f.write("""
  </ul>
</body>
</html>
""")
    print(f"Generated TOC at {toc_path}")

def main():
    for cmd in commands:
        generate_html_man_page(cmd)
    generate_toc()

if __name__ == "__main__":
    main()
