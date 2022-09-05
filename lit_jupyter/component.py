import sys
import os
import lightning as L
from typing import Optional
import subprocess
import shlex
from time import sleep

R_INSTALL = """
sudo apt-get update
sudo apt-get install r-base
sudo R -e "install.packages('IRkernel')"
Rscript -e 'IRkernel::installspec()'
""".split('\n')

JULIA_INSTALL = """
sudo apt-get update
wget https://julialang-s3.julialang.org/bin/linux/x64/1.7/julia-1.7.3-linux-x86_64.tar.gz
tar -xvzf julia-1.7.3-linux-x86_64.tar.gz; julia-1.7.3/bin/julia -e 'using Pkg; Pkg.add("IJulia")'
rm -rf julia-1.7.3-linux-x86_64.tar.gz
""".split('\n')


class CustomBuildConfig(L.BuildConfig):
    def __init__(self, kernel = str):
        self.kernel = kernel

    def build_commands(self):
        build_dict = {"python":[], "r":  R_INSTALL, "julia": JULIA_INSTALL}
        build_args = []

        for i in self.kernel.split("|"):
            if i in build_dict:
                build_args += build_dict[i]
        return ["pip3 install jupyterlab notebook"] + build_args


class JupyterLab(L.LightningWork):
    def __init__(self, kernel:str = None, cloud_compute: Optional[L.CloudCompute] = None, parallel=True):
        super().__init__(cloud_compute=cloud_compute, cloud_build_config=CustomBuildConfig(kernel), parallel=parallel)
        self.jupyter_url = None
        self.path = None
        self._process = None

    def run(self):
        # Generate new configuration
        os.system(f"{sys.executable} -m notebook --generate-config -y")

        # Jupyter Lab Configuration
        iframe_tornado_settings = """{\"headers\":{\"Content-Security-Policy\":\"frame-ancestors * 'self' "}}"""
        jupyter_config = f"--NotebookApp.token='' --NotebookApp.password='' --NotebookApp.tornado_settings='{iframe_tornado_settings}'"

        # Start Jupyter Lab
        with open(f"jupyter_lab_{self.port}", "w") as f:
            self._process = subprocess.Popen(
                shlex.split(f"{sys.executable} -m jupyter lab --ip {self.host} --port {self.port} --no-browser {jupyter_config}"),
                bufsize=0,
                close_fds=True,
                stdout=f,
                stderr=f,
            )

        # wait 5 seconds until server starts, Open log file
        sleep(5)

        # Extract token
        with open(f"jupyter_lab_{self.port}") as f:
            lines = f.readlines()
            for line in lines:
                if f'{self.port}/lab' in line:
                    self.jupyter_url = line.split(' ')[-1].strip()
