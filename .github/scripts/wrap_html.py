def wrap_html(file_path):
    with open(file_path) as f:
        content = f.read()

    wrapped = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>enclov man page</title>
  <style>
    body {{ font-family: monospace; padding: 2rem; background: #fdfdfd; color: #111; }}
    pre {{ background: #eee; padding: 1rem; overflow-x: auto; }}
    h1, h2 {{ border-bottom: 1px solid #ccc; }}
  </style>
</head>
<body>
  <h1>Enclov CLI Manual</h1>
  <pre>{content}</pre>
</body>
</html>"""
    
    with open(file_path, "w") as f:
        f.write(wrapped)
    print(f"Wrapped HTML saved to {file_path}")
