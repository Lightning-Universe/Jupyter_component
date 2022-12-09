import os
import shlex
import subprocess
import sys
from time import sleep
from typing import Optional, Literal
from dataclasses import dataclass
import lightning as L

R_INSTALL: list = """
sudo apt-get update
sudo apt-get install r-base
sudo R -e "install.packages('IRkernel')"
Rscript -e 'IRkernel::installspec()'
""".split(
    "\n"
)

JULIA_INSTALL: list = """
sudo apt-get update
wget https://julialang-s3.julialang.org/bin/linux/x64/1.7/julia-1.7.3-linux-x86_64.tar.gz
tar -xvzf julia-1.7.3-linux-x86_64.tar.gz; julia-1.7.3/bin/julia -e 'using Pkg; Pkg.add("IJulia")'
rm -rf julia-1.7.3-linux-x86_64.tar.gz
""".split(
    "\n"
)


@dataclass
class CustomBuildConfig(L.BuildConfig):
    
    kernel: str = "python"

    def build_commands(self) -> list:
        build_dict = {"python": [], "r": [R_INSTALL], "julia": [JULIA_INSTALL]}
        return ["pip3 install jupyterlab notebook"] + build_dict[self.kernel]


class JupyterLab(L.LightningWork):
    def __init__(self, kernel: Literal["python", "r", "julia"] = "python", cloud_compute: Optional[L.CloudCompute] = None, parallel: bool = True) -> None:
        super().__init__(cloud_compute=cloud_compute, cloud_build_config=CustomBuildConfig(kernel), parallel=parallel)
        self.jupyter_url = None
        self.path = None
        self._process = None

    def run(self) -> None:
        # Generate new configuration
        os.system(f"{sys.executable} -m notebook --generate-config -y")

        # Jupyter Lab Configuration
        iframe_tornado_settings = """{\"headers\":{\"Content-Security-Policy\":\"frame-ancestors * 'self' "}}"""
        jupyter_config = (
            "--NotebookApp.token=''"
            " --NotebookApp.password=''"
            f" --NotebookApp.tornado_settings='{iframe_tornado_settings}'"
        )

        # Start Jupyter Lab
        with open(f"jupyter_lab_{self.port}", "w") as fp:
            self._process = subprocess.Popen(  # type: ignore
                shlex.split(
                    f"{sys.executable} -m jupyter lab --ip {self.host} --port {self.port} --no-browser {jupyter_config}"
                ),
                bufsize=0,
                close_fds=True,
                stdout=fp,
                stderr=fp,
            )

        # wait 5 seconds until server starts, Open log file
        sleep(5)

        # Extract token
        with open(f"jupyter_lab_{self.port}") as fp:
            lines = fp.readlines()
        for line in lines:
            if f"{self.port}/lab" in line:
                self.jupyter_url = line.split(" ")[-1].strip()  # type: ignore
