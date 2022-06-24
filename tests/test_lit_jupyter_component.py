from unittest import mock
from lit_jupyter.component import LitJupyter


@mock.patch("lit_jupyter.component.subprocess.Popen")
def test_subprocess(mock_popen):
    mock_popen().wait.return_value = 0
    lightning_work = LitJupyter()
    lightning_work.run()
    return mock_popen.assert_called()
