import logging
import subprocess
import os
import subprocess
import sys
import lightning as L
from typing import Optional
from lightning.app.storage import Path


class JupyterWork(L.LightningWork):
    def __init__(self, cloud_compute: Optional[L.CloudCompute] = None):
        super().__init__(cloud_compute=cloud_compute, parallel=True)
        self.pid = None
        self.exit_code = None
        self.storage = None


    def run(self):
        # Delete Existing Configuration
        self.storage = Path(".")
        jupyter_notebook_config_path = Path.home() / ".jupyter/jupyter_notebook_config.py"
        if os.path.exists(jupyter_notebook_config_path):
            os.remove(jupyter_notebook_config_path)

        # Generate new configuration
        with subprocess.Popen(
            f"{sys.executable} -m notebook --generate-config".split(" "),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=0,
            close_fds=True,
        ) as proc:
            self.pid = proc.pid

            self.exit_code = proc.wait()
            if self.exit_code != 0:
                raise Exception(self.exit_code)

        # Add iFrame configuration
        with open(jupyter_notebook_config_path, "a") as f:
            f.write(
                """c.NotebookApp.tornado_settings = {'headers': {'Content-Security-Policy': "frame-ancestors * 'self' "}}"""  # noqa E501
            )

        # Start jupyter without password
        remove_pwd = f"--NotebookApp.token='' --NotebookApp.password=''"
        with open(f"jupyter_lab_{self.port}", "w") as f:
            proc = subprocess.Popen(
                f"{sys.executable} -m jupyter lab --ip {self.host} --port {self.port} --no-browser {remove_pwd}".split(" "),
                bufsize=0,
                close_fds=True,
                stdout=f,
                stderr=f,
            )

class JupyterLabManager(L.LightningFlow):
    def __init__(self) -> None:
        super().__init__()
        self.user_name = 'JupyterLab'
        self.jupyter_work = JupyterWork(cloud_compute=L.CloudCompute(os.getenv("COMPUTE", "cpu")))

    def run(self):
        self.jupyter_work.run()
    
    def configure_layout(self):
        return {'name': f"{self.user_name}", 'content': self.jupyter_work}

app = L.LightningApp(JupyterLabManager())
