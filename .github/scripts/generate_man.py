import subprocess
import datetime
import os

def generate_man_page(command_name, version="1.0.0", section="1"):
    try:
        help_output = subprocess.check_output([command_name, '--help'], text=True)
    except Exception as e:
        print(f"Failed to run `{command_name} --help`: {e}")
        return

    today = datetime.datetime.now().strftime("%B %Y")
    man_page = [
        f".TH {command_name.upper()} {section} \"{today}\" \"v{version}\" \"{command_name.capitalize()} Manual\"",
        ".SH NAME",
        f"{command_name} \\- auto-generated man page",
        ".SH SYNOPSIS",
        f".B {command_name} [options]",
        ".SH DESCRIPTION",
        "Auto-generated from `--help` output:",
        ".nf",
        *(line.replace("\\", "\\\\") for line in help_output.strip().splitlines()),
        ".fi"
    ]

    os.makedirs("man", exist_ok=True)
    man_filename = f"man/{command_name}.1"
    with open(man_filename, "w") as f:
        f.write("\n".join(man_page))

    print(f"Generated man page: {man_filename}")

if __name__ == "__main__":
    generate_man_page("enclov")
