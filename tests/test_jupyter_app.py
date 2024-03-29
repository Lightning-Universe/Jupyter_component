import os

import requests
from lightning.app import CloudCompute, LightningApp, LightningFlow
from lightning.app.runners import MultiProcessRuntime

from lai_jupyter import JupyterLab


class TestJupyterServer(LightningFlow):
    def __init__(self):
        super().__init__()
        self.success = False

    def run(self, jupyter_url: str):
        response = requests.get(jupyter_url)
        if response.status_code == 200:
            self.success = True


class RootFlow(LightningFlow):
    def __init__(self):
        super().__init__()
        self.jupyter_work = JupyterLab(
            kernel="python", cloud_compute=CloudCompute(os.getenv("LIGHTNING_JUPYTER_LAB_COMPUTE", "cpu-small"))
        )
        self.test_jupyter_flow = TestJupyterServer()

    def run(self):
        self.jupyter_work.run()
        if self.jupyter_work.jupyter_url:
            self.test_jupyter_flow.run(self.jupyter_work.jupyter_url)

        if self.test_jupyter_flow.success:
            print("Test successful, Exiting")
            self._exit()

    def configure_layout(self):
        return {"name": "TestServer", "content": self.jupyter_work}


def test_file_server():
    app = LightningApp(RootFlow())
    MultiProcessRuntime(app).dispatch()
