from unittest import mock
from lit_jupyter.component import LitJupyter


@mock.patch("lit_jupyter.component.subprocess.run")
def test_subprocess(mock_popen):
    mock_popen().wait.return_value = 0
    obj1 = LitJupyter()
    obj1.run()
    return mock_popen.assert_called()
