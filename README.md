<div align="center">
<img src="https://jupyter.org/assets/homepage/main-logo.svg" width="200px">

A Lightning component to Launch Jupyter Lab
______________________________________________________________________

![Tests](https://github.com/Lightning-AI/LAI-Jupyter-Component/actions/workflows/ci-testing.yml/badge.svg)
</div>

# Jupyter Lab
JupyterLab is the latest web-based interactive development environment for notebooks, code, and data. Its flexible interface allows users to configure and arrange workflows in data science, scientific computing, computational journalism, and machine learning. This component allows you to create `LightningWork` with Jupyter Lab. This components support the following jupyter kernels (`Python 3.8`, `R 3,6` and `Julia 1.7`).

## Usage
To use this component add modify the following variables below. Please consider checking out our documentation to understand they types of [Cloud Compute](https://lightning.ai/lightning-docs/core_api/lightning_work/compute.html) instances supported. Startup time for this component with all kernels is around `5-6` minutes.

```python
from lai_jupyter import JupyterLab
import lightning as L
import os


class RootFlow(L.LightningFlow):
    def __init__(self) -> None:
        super().__init__()
        self.jupyter_work = JupyterLab(kernel=os.getenv("LIGHTNING_JUPYTER_LAB_KERNEL", "python"),
                                       cloud_compute=L.CloudCompute(
                                           os.getenv("LIGHTNING_JUPYTER_LAB_COMPUTE", "cpu-small")))

    def run(self):
        self.jupyter_work.run()

    def configure_layout(self):
        return {'name': "JupyterLab", 'content': self.jupyter_work}


app = L.LightningApp(RootFlow())
```

By default this component launches with `cpu-small` [Compute Instance](https://lightning.ai/lightning-docs/core_api/lightning_work/compute.html) and `python` Kernel. This can be overridden using the `LIGHTNING_JUPYTER_LAB_COMPUTE` and `LIGHTNING_JUPYTER_LAB_KERNEL` environment variable.


```
lightning run app demo_app.py --cloud
lightning run app demo_app.py --cloud --env LIGHTNING_JUPYTER_LAB_COMPUTE=gpu
lightning run app demo_app.py --cloud --env LIGHTNING_JUPYTER_LAB_COMPUTE=gpu --env LIGHTNING_JUPYTER_LAB_KERNEL="python|r|julia"
```


## Installation
Use these instructions to install:

```
lightning install component lightning/LAI-Jupyter-Component
```

Or use it with pip
```
> cat requirements.txt
git+https://github.com/Lightning-AI/LAI-Jupyter-Component
```

Or to build locally
```bash
git clone https://github.com/Lightning-AI/LAI-Jupyter-Component

cd LAI-Jupyter-Component
pip install .
```

## Tests
To run the test locally:
```
# From the root of this package
pip install -r tests/requirements.txt
pytest
```
