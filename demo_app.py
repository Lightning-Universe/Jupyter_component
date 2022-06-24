from lit_jupyter import LitJupyter
import lightning as L
import os


class JupyterLabManager(L.LightningFlow):
    def __init__(self) -> None:
        super().__init__()
        self.jupyter_work = LitJupyter(cloud_compute=L.CloudCompute(os.getenv("COMPUTE", "cpu-small")))

    def run(self):
        self.jupyter_work.run()
    
    def configure_layout(self):
        return [{'name': "JupyterLab", 'content': self.jupyter_work}]

app = L.LightningApp(JupyterLabManager())
