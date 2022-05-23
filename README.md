# lit_jupyter component

This ⚡ [Lightning component](lightning.ai) ⚡ was generated automatically with:

```bash
lightning init component lit_jupyter
```

## To run lit_jupyter

First, install lit_jupyter (warning: this app has not been officially approved on the lightning gallery):

```bash
lightning install component https://github.com/PyTorchLightning/lit-jupyter
```

Once the app is installed, use it in an app:

```python
from lit_jupyter import LitJupyter
import lightning as L


class LitApp(L.LightningFlow):
    def __init__(self) -> None:
        super().__init__()
        self.lit_jupyter = LitJupyter()

    def run(self):
        self.lit_jupyter.run()
    
    def configure_layout(self):
        return {'name': 'notebook', 'content': self.lit_jupyter}

app = L.LightningApp(LitApp())

```
