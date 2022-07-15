import os

from lightning_app import LightningApp
import pytest
import requests
import lightning as L
from time import sleep
from lit_jupyter import JupyterLab
from lightning_app.testing.testing import run_app_in_cloud, wait_for
from lightning.app.runners import MultiProcessRuntime


class TestJupyterServer(L.LightningFlow):
    def __init__(self):
        super().__init__()
        self.success = False 

    def run(self, jupyter_url: str):
        response = requests.get(jupyter_url)    
        if response.status_code == 200:
            self.success = True


class RootFlow(L.LightningFlow):
    def __init__(self):
        super().__init__()
        self.jupyter_work = JupyterLab(kernel="python", cloud_compute=L.CloudCompute(os.getenv("COMPUTE", "cpu-small")))
        self.test_jupyter_flow = TestJupyterServer()

    def run(self):
        self.jupyter_work.run()
        print("Running.....")

        print(self.jupyter_work.jupyter_url)
        if self.jupyter_work.jupyter_url:
            self.test_jupyter_flow.run(self.jupyter_work.jupyter_url)
        
        if self.test_jupyter_flow.success:
            print("Test successful, Exiting")
            self._exit()

    def configure_layout(self):
        return {"name": "TestServer", "content": self.jupyter_work}


def test_file_server():
    app = L.LightningApp(RootFlow())
    MultiProcessRuntime(app).dispatch()


@pytest.mark.cloud
def test_app_example_cloud() -> None:
    with run_app_in_cloud(app_folder=os.path.dirname(__file__), app_name=os.path.basename(__file__)) as (
        _,
        view_page,
        _,
    ):
        def click_button(*_, **__):
            button = view_page.locator(f'button:has-text("TESTSERVER")')
            button.wait_for(timeout=3 * 1000)
            button.click()
            return True
        
        wait_for(view_page, click_button)

if __name__ == "__main__":
    app = LightningApp(RootFlow())