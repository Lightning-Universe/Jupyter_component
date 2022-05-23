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
