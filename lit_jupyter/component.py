import logging
import sys
import os
import lightning as L
from typing import Optional
import subprocess
import shlex


pkg_install_r = """
sudo apt install r-base
sudo R -e "install.packages('IRkernel')"
Rscript -e "IRkernel::installspec()"
""".split('\n')

pkg_install_julia = """
wget https://julialang-s3.julialang.org/bin/linux/x64/1.7/julia-1.7.3-linux-x86_64.tar.gz
tar -xvzf julia-1.7.3-linux-x86_64.tar.gz; julia-1.7.3/bin/julia -e 'using Pkg; Pkg.add("IJulia")'
rm -rf julia-1.7.3-linux-x86_64.tar.gz
""".split('\n')


class CustomBuildConfig(L.BuildConfig):
    def __init__(self, kernel = str):
        self.requirements = ["jupyterlab", "notebook"]
        self.kernel = kernel

    def build_commands(self):
        build_dict = {"python":[], "r":  pkg_install_r, "julia": pkg_install_julia}
        build_args = []

        for i in self.kernel.split("|"):
            if i in build_dict:
                build_args += build_dict[i]
        return build_args


class JupyterLab(L.LightningWork):
    def __init__(self, kernel:str = None, cloud_compute: Optional[L.CloudCompute] = None):
        super().__init__(cloud_compute=cloud_compute, cloud_build_config=CustomBuildConfig(kernel), parallel=True)
        self.token = None

    # 1 min startup time
    def run(self):
        # Generate new configuration
        os.system(f"{sys.executable} -m notebook --generate-config")

        # Jupyter Lab Configuration
        iframe_tornado_settings = """{\"headers\":{\"Content-Security-Policy\":\"frame-ancestors * 'self' "}}"""
        jupyter_config = f"--NotebookApp.token='' --NotebookApp.password='' --NotebookApp.tornado_settings='{iframe_tornado_settings}'"

        # Start Jupyter Lab
        with open(f"jupyter_lab_{self.port}", "w") as f:
            proc = subprocess.Popen(
                shlex.split(f"{sys.executable} -m jupyter lab --ip {self.host} --port {self.port} --no-browser {jupyter_config}"),
                bufsize=0,
                close_fds=True,
                stdout=f,
                stderr=f,
            )
        
        # Extract URL
        with open(f"jupyter_lab_{self.port}") as f:
            while True:
                for line in f.readlines():
                    if "lab?token=" in line:
                        self.token = line.split("lab?token=")[-1]
                        proc.wait()
