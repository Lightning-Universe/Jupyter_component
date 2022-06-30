from unittest import mock
import pytest
from lit_jupyter.component import JupyterLab
from lightning_app.testing.testing import application_testing, LightningTestApp
from lightning_app.utilities.enum import AppStage
from typing import Tuple
import os
from click.testing import CliRunner
from lightning_app.cli.lightning_cli import run_app



@mock.patch("lit_jupyter.component.subprocess.Popen")
def test_subprocess(mock_popen):
    mock_popen().wait.return_value = 0
    lightning_work = JupyterLab()
    lightning_work.run()
    return mock_popen.assert_called()


def test_e2e_integration():
    runner = CliRunner()

    command_line = [
        os.path.join("../demo_app.py"),
        "--blocking",
        "False",
        "--multiprocess",
        "--open-ui",
        "False",
    ]
    result = runner.invoke(run_app, command_line, catch_exceptions=False)
    assert result.exit_code == 0
