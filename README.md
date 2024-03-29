<div align="center">
<img src="https://jupyter.org/assets/homepage/main-logo.svg" width="200px">

A Lightning component to Launch Jupyter Lab

______________________________________________________________________

[![Lightning](https://img.shields.io/badge/-Lightning-792ee5?logo=pytorchlightning&logoColor=white)](https://lightning.ai)
![license](https://img.shields.io/badge/License-Apache%202.0-blue.svg)
![Tests](https://github.com/Lightning-AI/LAI-Jupyter-Component/actions/workflows/ci-testing.yml/badge.svg)

</div>

# Jupyter Lab

JupyterLab is the latest web-based interactive development environment for notebooks, code, and data. Its flexible interface allows users to configure and arrange workflows in data science, scientific computing, computational journalism, and machine learning. This component allows you to create `LightningWork` with Jupyter Lab. This components support the following jupyter kernels (`Python 3.8`, `R 3,6` and `Julia 1.7`).

## Usage

To use this component add modify the following variables below. Please consider checking out our documentation to understand they types of [Cloud Compute](https://lightning.ai/lightning-docs/core_api/lightning_work/compute.html) instances supported. Startup time for this component with all kernels is around `5-6` minutes.

```python
import lightning as L
from lai_jupyter import JupyterLab

app = L.LightningApp(JupyterLab(cloud_compute=L.CloudCompute("cpu-small")))
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
lightning install component lightning/lit-jupyter
```

Or use it with pip

```
pip install lightning-jupyter
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
