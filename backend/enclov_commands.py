# enclov_commands.py

def enclov_version():
    return "Enclov CLI v1.0.2"

def enclov_start():
    return "Engine started 🚀"

def enclov_config():
    return '''{
  "env": "production",
  "autosync": true
}'''

def enclov_help():
    return """
Available Commands:
  - enclov version
  - enclov start
  - enclov config
  - enclov help
"""

allowed_funcs = {
    "enclov version": enclov_version,
    "enclov start": enclov_start,
    "enclov config": enclov_config,
    "enclov help": enclov_help,
}
