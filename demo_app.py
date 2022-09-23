#!/usr/bin/env python3

import os

import lightning as L

from lit_jupyter import JupyterLab


class JupyterLabManager(L.LightningFlow):
    def __init__(self) -> None:
        super().__init__()
        self.jupyter_work = JupyterLab(
            kernel=os.getenv("LIGHTNING_JUPYTER_LAB_KERNEL", "python"),
            cloud_compute=L.CloudCompute(os.getenv("LIGHTNING_JUPYTER_LAB_COMPUTE", "cpu-small")),
        )

    def run(self):
        self.jupyter_work.run()

    def configure_layout(self):
        return [{"name": "JupyterLab", "content": self.jupyter_work}]


app = L.LightningApp(JupyterLabManager())
