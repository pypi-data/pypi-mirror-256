from typing import List
import subprocess
import os
import tempfile
from dataclasses import dataclass
import venv

from actuate.core import action, workflow


@dataclass
class ExecutionResult:
    stdout: str
    stderr: str
    exit_status: int


@workflow(
    name=lambda: "Run Python code",
)
async def run_python_code(code: str, requirements: str) -> ExecutionResult:
    """Run python code in a virtual environment.
    :param code: The code to execute. All stdout will be captured and returned.
    :param requirements: A string containing the python requirements. Each requirement should be separated by a newline.
    """
    reqs = requirements.split("\n")
    reqs = [req.strip() for req in reqs if req.strip()]
    temp_dir_path = tempfile.mkdtemp()
    with tempfile.TemporaryDirectory() as temp_dir_path:
        venv_path = os.path.join(temp_dir_path, "venv")
        await _create_venv(venv_path)
        if reqs:
            await _install_requirements(venv_path, reqs)
        result = await _run_code(temp_dir_path, venv_path, code)
        return result


@action()
async def _create_venv(venv_path: str):
    """The agt CLI needs to create the venv using the embedded Python executable running this code.
    Otherwise we get a failure on pip install."""
    actuate_bin_path = os.environ.get("AGENTIC_BIN_PATH")
    if not actuate_bin_path:
        raise ValueError(
            "AGENTIC_BIN_PATH environment variable not set. This is required for creating a Python virtual env."
        )
    subprocess.run(
        [actuate_bin_path, "create-python-venv", venv_path],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


@action()
async def _install_requirements(venv_path: str, reqs: List[str]):
    pip_exe = os.path.join(venv_path, "bin", "pip")
    for req in reqs:
        if not req:
            continue
        subprocess.run(
            [pip_exe, "install", req],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )


@action()
async def _run_code(temp_dir_path: str, venv_path: str, code: str):
    with open(os.path.join(temp_dir_path, "code.py"), "w") as f:
        f.write(code)
    py_exe = os.path.join(venv_path, "bin", "python")
    result = subprocess.run(
        [py_exe, os.path.join(temp_dir_path, "code.py")],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout = result.stdout.decode()
    stderr = result.stderr.decode()
    return ExecutionResult(stdout=stdout, stderr=stderr, exit_status=result.returncode)
