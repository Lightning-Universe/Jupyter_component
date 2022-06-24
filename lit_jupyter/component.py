import logging
import subprocess
import sys
import os
import lightning as L
from typing import Optional
from pathlib import Path


class LitJupyter(L.LightningWork):
    def __init__(self, cloud_compute: Optional[L.CloudCompute] = None):
        super().__init__(cloud_compute=cloud_compute, parallel=True)
        self.exit_code = None
        self.storage = None

    def run(self):
        jupyter_out = open('jupyter_log.txt', 'a')

        # Delete Existing Configuration
        jupyter_notebook_config_path = Path.home() / ".jupyter/jupyter_notebook_config.py"
        if os.path.exists(jupyter_notebook_config_path):
            os.remove(jupyter_notebook_config_path)

        # Generate new configuration
        proc_config =  subprocess.Popen(
            f"{sys.executable} -m notebook --generate-config".split(" "),
            stdout=jupyter_out,
            stderr=jupyter_out,
            bufsize=0,
            close_fds=True)
        proc_config.wait()
  
        # Add iFrame configuration
        with open(jupyter_notebook_config_path, "a") as f:
            f.write(
                """c.NotebookApp.tornado_settings = {'headers': {'Content-Security-Policy': "frame-ancestors * 'self' "}}"""  # noqa E501
            )

        # Start jupyter without password
        remove_pwd = f"--NotebookApp.token='' --NotebookApp.password=''"
        proc_server = subprocess.Popen(
            f"{sys.executable} -m jupyter lab --ip {self.host} --port {self.port} --no-browser {remove_pwd}".split(" "),
            stdout=jupyter_out,
            stderr=jupyter_out,
            bufsize=0,
            close_fds=True
        )
        proc_server.wait()
