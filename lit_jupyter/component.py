import logging
import subprocess
import lightning as L

logger = logging.getLogger(__name__)

class LitJupyter(L.LightningWork):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, parallel=True, **kwargs)

    def run(self):
        remove_pwd = "--NotebookApp.token='' --NotebookApp.password=''"
        host_info = f"--ip={self.host} --port={self.port}"
        cmd = f"jupyter-lab --allow-root --no-browser {host_info} {remove_pwd}"
        subprocess.run(cmd, shell=True)