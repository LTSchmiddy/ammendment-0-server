# This method in the utils module is gonna be really helpful here:
import sys, os, json, subprocess, shutil

import Cython
from src.py.utils import get_dir_tree, list_get
from src.py.utils import anon_func as af

# from src.py import settings
# settings.load_settings()

from distutils.core import setup, Extension
from Cython.Build import *
from Cython.Compiler.Errors import CompileError

python_suffix = ".py"
cython_suffix = ".pyx"
source_dir = "./src/py"
out_dir = "./cython_build"

delete_unneeded_files = True

platform_extension = af.tget(os.name == 'nt', ".pyd", ".so")

if os.path.isdir(out_dir):
    shutil.rmtree(out_dir)
    
shutil.copytree(source_dir, out_dir)

def handle_entry(name: str, fullpath: str, parent_dir: str):
    # print(fullpath)
    if name.endswith(python_suffix):
        filename = classname = name.removesuffix(python_suffix)
        dst_path = os.path.join(parent_dir, filename)
        
        if classname == "__init__":
            classname = parent_dir.replace("\\", "/").split("/")[-1]
        
        try:
            compile_cython(classname, fullpath)
            # Moving File:
            outname = list_get(lambda x: x.startswith(classname) and x.endswith(platform_extension), os.listdir("./"))
            # print(outname)
            dst_path = os.path.join(parent_dir, filename)
            shutil.move(outname, dst_path + platform_extension)
            
            # Rename the source .py file, to avoid confusion on importing:
            if delete_unneeded_files:
                if os.path.isfile(dst_path + python_suffix): os.remove(dst_path + python_suffix)
                if os.path.isfile(dst_path + ".c"): os.remove(dst_path + ".c")
            else:
                os.rename(dst_path + python_suffix, dst_path + ".old_py")
            
        except CompileError as e:
            print(e)
            print("Using .py file directly")
            if os.path.isfile(dst_path + ".c"): os.remove(dst_path + ".c")
            

def compile_cython(classname, path):
    new_extension = Extension(classname, [path])
    setup(
        name=classname,
        ext_modules=cythonize(
            new_extension,
            compiler_directives={'language_level' : "3"}
        )
    )
    
    
dirtree = get_dir_tree(out_dir, handle_entry)

# Creating Entrypoint File:
entry_file = open("cython_build/a_zero_start.py", 'w')
# entry_file.write("import a_zero; a_zero.main()")
entry_file.write("import a_zero; app=a_zero.app")
entry_file.close()

print("Complete!")