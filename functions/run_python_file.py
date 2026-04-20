import os
import subprocess

from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file in a specified directory relative to the working directory, providing output and error information",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Directory path to execute the Python file from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)


def run_python_file(working_directory, file_path, args=None):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.normpath(os.path.join(abs_working_dir, file_path))

        if os.path.commonpath([abs_working_dir, abs_file_path]) != abs_working_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(abs_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not abs_file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", abs_file_path]

        if args:
            command.extend(args)

        subproc = subprocess.run(
            args=command,
            text=True,
            cwd=abs_working_dir,
            timeout=30,
            capture_output=True,
        )
        output = ""
        if subproc.returncode != 0:
            output += f"Process exited with code {subproc.returncode}\n"

        if not subproc.stderr and not subproc.stdout:
            output += "No output produced\n"
        else:
            output += f"STDOUT:{subproc.stdout}\n"
            output += f"STDERR:{subproc.stderr}\n"
        return output
    except Exception as e:
        return f"Error: executing Python file: {e}"
