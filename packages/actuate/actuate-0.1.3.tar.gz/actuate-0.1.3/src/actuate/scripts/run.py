import sys
import os
import importlib
import inspect

from typing import Any

from actuate.core.run_workflow import run_workflow_main


dir_path = os.path.dirname(os.path.realpath(__file__))
cwd = os.getcwd()

sys.path.insert(0, cwd)
sys.path.insert(0, dir_path)


def _get_workflow_module(wf: str):
    selected_module = None
    selected_main = None
    for path in ["workflows"]:
        try:
            path = f"{path}.{wf}"
            selected_module = importlib.import_module(path)
        except ModuleNotFoundError as e:
            if wf in str(e):
                continue
            raise e
        selected_main = getattr(selected_module, "main", None)
    assert selected_module is not None, f"Task {wf} not found"
    assert selected_main is not None, f"Task {wf} does not have a main function"
    return selected_module


def run_selected_main(*args: Any):
    from .make_cli import make_cli_and_get_args

    wf = args[0]
    wf_modified = wf.replace("-", "_")
    selected_module = _get_workflow_module(wf_modified)
    workflow_main = getattr(selected_module, "main", None)
    assert workflow_main, f"Workflow {selected_module} does not have a main function"
    args = args[1:]
    parsed = make_cli_and_get_args(wf, workflow_main, args)
    run_workflow_main(workflow_main, *parsed)


if __name__ == "__main__":
    run_selected_main(*sys.argv[1:])
