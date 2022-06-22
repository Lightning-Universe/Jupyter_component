import os
import logging
import lightning as L
from lightning.app.runners import SingleProcessRuntime
from lit_jupyter.component import LitJupyter


class JupyterLabManager(L.LightningFlow):
    def __init__(self) -> None:
        super().__init__()
        self.user_name = 'JupyterLab'
        self.jupyter_work = LitJupyter(cloud_compute=L.CloudCompute(idle_timeout=5))

    def run(self):
        self.jupyter_work.run()
    
    def configure_layout(self):
        return {'name': f"{self.user_name}", 'content': self.jupyter_work}


def test_jupyter_lab(caplog):
    caplog.set_level(logging.INFO)
    logger = logging.getLogger('app')
    logger.propagate = True

    app = L.LightningApp(JupyterLabManager())
    SingleProcessRuntime(app, start_server=False).dispatch()
    #lit_jupyter_lab = LitJupyter()
    #print(caplog.text)
