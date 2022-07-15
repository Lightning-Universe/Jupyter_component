<div align="center">
<img src="https://jupyter.org/assets/homepage/main-logo.svg" width="200px">

A Lightning component to Launch Jupyter Lab
______________________________________________________________________

![Tests](https://github.com/PyTorchLightning/LAI-Jupyter-Component/actions/workflows/ci-testing.yml/badge.svg)
</div>

# Jupyter Lab
JupyterLab is the latest web-based interactive development environment for notebooks, code, and data. Its flexible interface allows users to configure and arrange workflows in data science, scientific computing, computational journalism, and machine learning. This component allows you to create `LightningWork` with Jupyter Lab. This components support the following jupyter kernels (`Python 3.8`, `R 3,6` and `Julia 1.7`).

# Usage
To use this component add modify the following variables below. Please consider checking out our documentation to understand they types of [Cloud Compute](https://lightning.ai/lightning-docs/core_api/lightning_work/compute.html) instances supported. Startup time for this component with all kernels is around `5-6` minutes.

```python
from lit_jupyter import JupyterLab
import lightning as L
import os

class RootFlow(L.LightningFlow):
    def __init__(self) -> None:
        super().__init__()
        self.jupyter_work = JupyterLab(kernel="python|julia|r", cloud_compute=L.CloudCompute(os.getenv("COMPUTE", "cpu-small")))

    def run(self):
        self.jupyter_work.run()
    
    def configure_layout(self):
        return {'name': "JupyterLab", 'content': self.jupyter_work}

app = L.LightningApp(RootFlow())
```

By default this component is launched using a `cpu-small` [Compute Instance](https://lightning.ai/lightning-docs/core_api/lightning_work/compute.html). This can be overridden using the COMPUTE environment variable.


```
lightning run app component.py --cloud
lightning run app component.py --cloud --env COMPUTE=gpu
```


# Installation
Use these instructions to install:

```
lightning install component lightning/LAI-Jupyter-Component
```

Or to build locally
```bash
git clone https://github.com/PyTorchLightning/LAI-Jupyter-Component
cd LAI-Jupyter-Component
pip install -r requirements.txt
pip install -e .
```

# Tests
To run the test locally:
```
# From the root of this package
pip install -r tests/requirements.txt
pytest
```
