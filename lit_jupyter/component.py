import logging
import subprocess
import sys
import os
import lightning as L
from typing import Optional
from pathlib import Path


pkg_install = """
sudo apt-get update
sudo apt install r-base
sudo R -e "install.packages('IRkernel')"
Rscript -e "IRkernel::installspec()"
wget https://julialang-s3.julialang.org/bin/linux/x64/1.7/julia-1.7.3-linux-x86_64.tar.gz
tar -xvzf julia-1.7.3-linux-x86_64.tar.gz; julia-1.7.3/bin/julia -e 'using Pkg; Pkg.add("IJulia")'
rm -rf julia-1.7.3-linux-x86_64.tar.gz
""".split('\n')


class CustomBuildConfig(L.BuildConfig):
    def build_commands(self):
        return pkg_install

class LitJupyter(L.LightningWork):
    def __init__(self, cloud_compute: Optional[L.CloudCompute] = None):
        build_config = CustomBuildConfig()
        super().__init__(cloud_compute=cloud_compute, cloud_build_config=build_config, parallel=True)

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
        if os.path.exists(jupyter_notebook_config_path):
            with open(jupyter_notebook_config_path, "a") as f:
                f.write(
                    """c.NotebookApp.tornado_settings = {'headers': {'Content-Security-Policy': "frame-ancestors * 'self' "}}"""
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
