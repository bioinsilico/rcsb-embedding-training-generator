import subprocess


def run_command(command):
    try:
        # Use subprocess.run to execute the command and capture the output
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        # Get the standard output
        stdout = result.stdout
        stderr = result.stderr
        if stderr:
            print(result.stderr.strip())
        # Return both stdout and stderr for further processing if needed
        return stdout, stderr

    except subprocess.CalledProcessError as e:
        raise Exception(f"Command '{command}' failed with error: {e}")
