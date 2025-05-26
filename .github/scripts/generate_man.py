import subprocess
import os

commands = ["start", "config", "version"]
html_dir = "docs"

os.makedirs(html_dir, exist_ok=True)

css = """
<style>
  body { background: #121212; color: #eee; font-family: 'Fira Mono', monospace; padding: 2rem; }
  a { color: #79b8ff; text-decoration: none; }
  a:hover { text-decoration: underline; }
  pre { background: #222; padding: 1rem; border-radius: 4px; overflow-x: auto; }
</style>
"""

def wrap_html(html_path):
    with open(html_path, "r") as f:
        content = f.read()
    wrapped = f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><title>Enclov CLI Manual</title>{css}</head>
<body><pre>{content}</pre></body>
</html>"""
    with open(html_path, "w") as f:
        f.write(wrapped)

for cmd in commands:
    man_file = f"man/enclov-{cmd}.1"
    html_file = os.path.join(html_dir, f"enclov-{cmd}.html")
    with open(html_file, "w") as html_out:
        subprocess.run(["groff", "-man", "-Thtml", man_file], stdout=html_out, check=True)
    wrap_html(html_file)
