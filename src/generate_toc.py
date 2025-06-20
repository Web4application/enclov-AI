commands = ["start", "config", "version"]

with open("docs/index.html", "w") as f:
    f.write("""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Enclov CLI Manual - Table of Contents</title>
  <style>
    body { font-family: monospace; background: #f0f0f0; padding: 2rem; }
    a { text-decoration: none; color: #007acc; }
    a:hover { text-decoration: underline; }
  </style>
</head>
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
print("Generated TOC at docs/index.html")
