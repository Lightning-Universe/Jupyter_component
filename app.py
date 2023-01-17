import lightning as L

from lai_jupyter import JupyterLab

app = L.LightningApp(JupyterLab(cloud_compute=L.CloudCompute("cpu-small")))
