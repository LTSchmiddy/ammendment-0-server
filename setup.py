import subprocess

subprocess.run([
    "python",
    "cythonizer.py",
    "build_ext",
    "--inplace"
])