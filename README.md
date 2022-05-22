# lit_jupyter component

This ⚡ [Lightning component](lightning.ai) ⚡ was generated automatically with:

```bash
lightning init component lit_jupyter
```

## To run lit_jupyter

First, install lit_jupyter (warning: this app has not been officially approved on the lightning gallery):

```bash
lightning install component https://github.com/theUser/lit_jupyter
```

Once the app is installed, use it in an app:

```python
from lit_jupyter import TemplateComponent
import lightning as L


class LitApp(L.LightningFlow):
    def __init__(self) -> None:
        super().__init__()
        self.lit_jupyter = TemplateComponent()

    def run(self):
        print(
            "this is a simple Lightning app to verify your component is working as expected"
        )
        self.lit_jupyter.run()


app = L.LightningApp(LitApp())
```
