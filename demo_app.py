#!/usr/bin/env python3

import os
import lightning as L
from lit_jupyter import JupyterLab

class JupyterLabManager(L.LightningFlow):
    def __init__(self) -> None:
        super().__init__()
        self.jupyter_work = JupyterLab(cloud_compute=L.CloudCompute(os.getenv("COMPUTE", "cpu-small")), kernel="python|r|julia")

    def run(self):
        self.jupyter_work.run()
        if os.environ['TEST']:
            self._exit("Application End!")
    
    def configure_layout(self):
        return [{'name': "JupyterLab", 'content': self.jupyter_work}]

app = L.LightningApp(JupyterLabManager())
