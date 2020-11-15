import subprocess

subprocess.run([
    "pip",
    "install",
    "-r"
    "_requirements.txt"
])

subprocess.run([
    "python",
    "cythonizer.py",
    "build_ext",
    "--inplace"
])

from distutils.core import setup

setup(
    name="a_zero",
    # package_dir="cython_build"
)