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