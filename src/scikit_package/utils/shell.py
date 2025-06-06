import subprocess


def run(command, cwd=None):
    """Run a shell command in the specified directory."""
    subprocess.run(
        command,
        check=True,
        shell=True,
        text=True,
        cwd=cwd,
    )
