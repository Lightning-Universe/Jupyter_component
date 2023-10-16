from lightning.app import CloudCompute, LightningApp

from lai_jupyter import JupyterLab

app = LightningApp(JupyterLab(cloud_compute=CloudCompute("cpu-small")))
