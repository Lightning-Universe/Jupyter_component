from lit_jupyter import TemplateComponent

import lightning as L


class LitApp(L.LightningFlow):
    def __init__(self) -> None:
        super().__init__()
        self.lit_jupyter = TemplateComponent()

    def run(self):
        print("this is a simple Lightning app to verify your component is working as expected")
        self.lit_jupyter.run()


app = L.LightningApp(LitApp())
