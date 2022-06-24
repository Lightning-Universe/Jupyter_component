import logging
import subprocess
import sys
import os
import lightning as L
from typing import Optional
from pathlib import Path
from subprocess import Popen, PIPE, STDOUT


class LitJupyter(L.LightningWork):
    def __init__(self, cloud_compute: Optional[L.CloudCompute] = None):
        super().__init__(cloud_compute=cloud_compute, parallel=True)

    
    def run(self):
        # Delete Existing Configuration
        jupyter_notebook_config_path = Path.home() / ".jupyter/jupyter_notebook_config.py"
        if os.path.exists(jupyter_notebook_config_path):
            os.remove(jupyter_notebook_config_path)

        # Generate new configuration
        cmd_config = f"{sys.executable} -m notebook --generate-config"
        Popen(cmd_config, shell=True)

        # Add iFrame configuration
        with open(jupyter_notebook_config_path, "a") as f:
            f.write(
                """c.NotebookApp.tornado_settings = {'headers': {'Content-Security-Policy': "frame-ancestors * 'self' "}}"""  # noqa E501
            )

        # Start jupyter without password
        remove_pwd = f"--NotebookApp.token='' --NotebookApp.password=''"
        cmd_server = f"{sys.executable} -m jupyter lab --ip {self.host} --port {self.port} --no-browser {remove_pwd}"
        subprocess.run(cmd_server, shell=True)

        logging.info(f'Notebook Stated')
