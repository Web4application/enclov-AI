import subprocess
import datetime

def generate_man_page(command_name, version="1.0.0", section="1"):
    # Get CLI help text
    try:
        help_output = subprocess.check_output([command_name, '--help'], text=True)
    except Exception as e:
        print(f"Failed to get help from `{command_name}`: {e}")
        return

    today = datetime.datetime.now().strftime("%B %Y")
    man_page = []

    # Header
    man_page.append(f".TH {command_name.upper()} {section} \"{today}\" \"v{version}\" \"{command_name.capitalize()} Manual\"")
    man_page.append(".SH NAME")
    man_page.append(f"{command_name} \\- auto-generated man page")
    man_page.append(".SH SYNOPSIS")
    man_page.append(f".B {command_name} [options]")
    man_page.append(".SH DESCRIPTION")
    man_page.append("Auto-generated from `--help` output:\n")

    # Format help output into Roff-compatible format
    man_page.append(".nf")  # no fill mode
    for line in help_output.strip().splitlines():
        man_page.append(line.replace("\\", "\\\\"))
    man_page.append(".fi")  # resume fill mode

    # Save to .1 file
    man_filename = f"{command_name}.1"
    with open(man_filename, "w") as f:
        f.write("\n".join(man_page))

    print(f"Man page generated: {man_filename}")
    print("View it with: man ./{}".format(man_filename))

# Usage
if __name__ == "__main__":
    generate_man_page("enclov")  # change this to your CLI command
