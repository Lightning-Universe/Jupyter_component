from unittest import mock
from lit_jupyter.component import JupyterLab
import os
from click.testing import CliRunner
from lightning_app.cli.lightning_cli import run_app


@mock.patch("lit_jupyter.component.subprocess.Popen")
def test_subprocess(mock_popen):
    mock_popen().wait.return_value = 0
    lightning_work = JupyterLab()
    lightning_work.run()
    return mock_popen.assert_called()
