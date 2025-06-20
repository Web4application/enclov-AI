import subprocess
import os

commands = [
    {"name": "start", "description": "Starts the enclov CLI environment."},
    {"name": "config", "description": "Manages enclov CLI configuration."},
    {"name": "version", "description": "Shows version info."},
]

output_dir = "docs"
images_dir = os.path.join(output_dir, "images")

if not os.path.exists(output_dir):
    os.makedirs(output_dir)
if not os.path.exists(images_dir):
    os.makedirs(images_dir)

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<title>enclov {cmd} command</title>
<style>
  body {{
    background: #121212;
    color: #eee;
    font-family: 'Fira Mono', monospace;
    padding: 2rem;
  }}
  h1, h2 {{
    color: #79b8ff;
  }}
  pre {{
    background: #222;
    padding: 1rem;
    border-radius: 4px;
    overflow-x: auto;
  }}
  img {{
    max-width: 100%;
    border: 1px solid #444;
    margin: 1rem 0;
    border-radius: 4px;
  }}
  a {{
    color: #79b8ff;
    text-decoration: none;
  }}
  a:hover {{
    text-decoration: underline;
  }}
</style>
</head>
<body>
  <h1>enclov {cmd} command</h1>
  <p>{description}</p>

  <h2>Usage Example</h2>
  <pre><code>$ enclov {cmd} --help</code></pre>

  <h2>Help Output</h2>
  <pre>{help_output}</pre>

  <!-- Example image, replace or remove if you don't have -->
  <h2>Example Output Screenshot</h2>
  <img src="images/enclov-{cmd}-output.png" alt="enclov {cmd} command output" />

  <p><a href="index.html">Back to Manual TOC</a></p>
</body>
</html>
"""

index_html = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<title>Enclov CLI Manual - Table of Contents</title>
<style>
  body {{
    background: #121212;
    color: #eee;
    font-family: 'Fira Mono', monospace;
    padding: 2rem;
  }}
  a {{
    color: #79b8ff;
    text-decoration: none;
    font-size: 1.2rem;
  }}
  a:hover {{
    text-decoration: underline;
  }}
  ul {{
    list-style: none;
    padding-left: 0;
  }}
  li {{
    margin-bottom: 1rem;
  }}
</style>
</head>
<body>
  <h1>Enclov CLI Manual</h1>
  <ul>
    {links}
  </ul>
</body>
</html>
"""

# Generate each command's HTML page
for cmd in commands:
    try:
        result = subprocess.run(["enclov", cmd["name"], "--help"], capture_output=True, text=True, check=True)
        help_text = result.stdout
    except Exception as e:
        help_text = f"Failed to get help output: {e}"

    filename = os.path.join(output_dir, f"enclov-{cmd['name']}.html")
    with open(filename, "w") as f:
        f.write(html_template.format(cmd=cmd["name"], description=cmd["description"], help_output=help_text.replace('<', '&lt;').replace('>', '&gt;')))

# Generate index.html with links
links_html = "\n".join([f'<li><a href="enclov-{cmd["name"]}.html">enclov {cmd["name"]} command</a></li>' for cmd in commands])

with open(os.path.join(output_dir, "index.html"), "w") as f:
    f.write(index_html.format(links=links_html))

print("Docs generated successfully!")
