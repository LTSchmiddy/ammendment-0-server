import subprocess, sys
 
subprocess.run([
    "python",
    "cythonizer.py",
    "build_ext",
    "--inplace"
])

if len(sys.argv) > 1:
    from distutils.core import setup
    setup(
        name="a_zero",
    )