import sys
import os
import lightning as L
from typing import Optional
import subprocess
import shlex
from time import sleep


R_INSTALL = """
sudo apt install r-base
sudo R -e "install.packages('IRkernel')"
Rscript -e 'IRkernel::installspec()'
""".split('\n')

JULIA_INSTALL = """
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
    def __init__(self, kernel:str = None, cloud_compute: Optional[L.CloudCompute] = None):
        super().__init__(cloud_compute=cloud_compute, cloud_build_config=CustomBuildConfig(kernel), parallel=True)
        self.jupyter_url = None

    def run(self):
        print("A")
        # Generate new configuration
        os.system(f"{sys.executable} -m notebook --generate-config")
        
        print("B")
        # Jupyter Lab Configuration
        iframe_tornado_settings = """{\"headers\":{\"Content-Security-Policy\":\"frame-ancestors * 'self' "}}"""
        jupyter_config = f"--NotebookApp.token='' --NotebookApp.password='' --NotebookApp.tornado_settings='{iframe_tornado_settings}'"

        print("C")
        # Start Jupyter Lab
        with open(f"jupyter_lab_{self.port}", "w") as f:
            proc = subprocess.Popen(
                shlex.split(f"{sys.executable} -m jupyter lab --ip {self.host} --port {self.port} --no-browser {jupyter_config}"),
                bufsize=0,
                close_fds=True,
                stdout=f,
                stderr=f,
            )
        
        # Sleep for a couple of seconds until server starts
        sleep(5)
        print("D")
        # Extract token
        with open(f"jupyter_lab_{self.port}") as f:
            lines = f.readlines()
            # Rewrite the URL
            for i in lines:
                if 'lightningwork'in i:
                    self.jupyter_url = i.split(' ')[-1].strip()

        print("E")
