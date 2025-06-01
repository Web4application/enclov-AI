import os

# Define all commands with their descriptions and options
commands = {
    "enclov": {
        "name": "enclov",
        "section": "1",
        "version": "v0.1.0",
        "date": "May 2025",
        "description": "privacy-first AI assistant CLI interface",
        "synopsis": "enclov [options] [commands]",
        "options": [
            ("--version", "Show version information."),
            ("--help", "Show this help message."),
        ],
        "commands": [
            ("start", "Start the Enclov AI container."),
            ("stop", "Stop the Enclov AI container."),
            ("status", "Show the current status of the container and services."),
            ("config [path]", "View or set configuration file path."),
            ("logs", "View real-time logs from the Enclov container."),
            ("update", "Update Enclov AI to the latest version."),
        ],
    },
    "start": {
        "name": "enclov-start",
        "section": "1",
        "version": "v0.1.0",
        "date": "May 2025",
        "description": "start Enclov AI container",
        "synopsis": "enclov start [options]",
        "options": [
            ("--help", "Show help for the start command."),
            ("--detached, -d", "Run container in detached/background mode."),
            ("--config <file>", "Specify path to configuration file."),
        ],
    },
    "stop": {
        "name": "enclov-stop",
        "section": "1",
        "version": "v0.1.0",
        "date": "May 2025",
        "description": "stop Enclov AI container",
        "synopsis": "enclov stop [options]",
        "options": [
            ("--help", "Show help for the stop command."),
            ("--force, -f", "Force stop immediately."),
        ],
    },
    "status": {
        "name": "enclov-status",
        "section": "1",
        "version": "v0.1.0",
        "date": "May 2025",
        "description": "show Enclov AI container and services status",
        "synopsis": "enclov status",
        "options": [
            ("--help", "Show help for the status command."),
        ],
    },
    "config": {
        "name": "enclov-config",
        "section": "1",
        "version": "v0.1.0",
        "date": "May 2025",
        "description": "manage Enclov configuration file",
        "synopsis": "enclov config [path]",
        "options": [
            ("--show", "Display the current config file path."),
            ("--set <path>", "Set a new config file path."),
            ("--help", "Show help for the config command."),
        ],
    },
    "logs": {
        "name": "enclov-logs",
        "section": "1",
        "version": "v0.1.0",
        "date": "May 2025",
        "description": "view Enclov AI container logs",
        "synopsis": "enclov logs [options]",
        "options": [
            ("--follow, -f", "Follow logs in real time."),
            ("--tail <n>", "Show only the last n lines of logs."),
            ("--help", "Show help for the logs command."),
        ],
    },
    "update": {
        "name": "enclov-update",
        "section": "1",
        "version": "v0.1.0",
        "date": "May 2025",
        "description": "update Enclov AI platform",
        "synopsis": "enclov update [options]",
        "options": [
            ("--check", "Check for updates without applying."),
            ("--force", "Force update, ignoring warnings."),
            ("--help", "Show help for the update command."),
        ],
    },
}

def generate_man_page(cmd):
    """Generate man page text for given command dictionary."""
    lines = []
    lines.append(f'.TH {cmd["name"].upper()} {cmd["section"]} "{cmd["date"]}" "{cmd["version"]}" "Enclov AI CLI Manual"')
    lines.append(f'.SH NAME\n{cmd["name"]} \\- {cmd["description"]}\n')
    lines.append(f'.SH SYNOPSIS\n.B {cmd["synopsis"]}\n')
    lines.append(f'.SH DESCRIPTION\n{cmd["description"]}\n')
    if "options" in cmd and cmd["options"]:
        lines.append('.SH OPTIONS')
        for opt, desc in cmd["options"]:
            lines.append(f'.TP\n.BR {opt}\n{desc}')
    if "commands" in cmd and cmd["commands"]:
        lines.append('.SH COMMANDS')
        for c, desc in cmd["commands"]:
            lines.append(f'.TP\n.B {c}\n{desc}')
    return '\n'.join(lines)

def save_man_pages(output_dir='man'):
    os.makedirs(output_dir, exist_ok=True)
    for key, cmd in commands.items():
        filename = os.path.join(output_dir, f'{cmd["name"]}.1')
        with open(filename, 'w') as f:
            f.write(generate_man_page(cmd))
        print(f'Generated man page: {filename}')

if __name__ == "__main__":
    save_man_pages()
