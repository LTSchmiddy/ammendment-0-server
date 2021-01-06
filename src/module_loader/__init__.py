from __future__ import annotations

import importlib.util
import os, sys
from typing import List
import settings
from types import ModuleType

from utils import anon_func as af, print_error

platform_extension = af.tget(os.name == 'nt', ".pyd", ".so")
module_extensions = ('.py', platform_extension)


class AZeroModuleWrapper:
    loaded: ModuleType = None
    module_type: str = ""
    args: str
    name: str
    path: str
    
    required_attrs: List[str] = ["init"]
    
    
    def __init__(self, host=None) -> None:
        super().__init__()
        
        self.args = settings.current["modules"]["core"][self.module_type]
        self.load_module(**self.args)
        
        self.inject_globals(host)
    
    @staticmethod
    def find_module_init(path: str):       
        for i in module_extensions:
            if path.endswith(i):
                if os.path.isfile(path):
                    print(f"Module root declared: {path}")
                    return path
                else:
                    raise FileNotFoundError(path)   
        
        init_path = path
        if os.path.isdir(path):
            init_path = os.path.join(path, "__init__").replace("\\", "/")
        
        for i in module_extensions:
            fullpath = init_path + i
            if os.path.isfile(fullpath):
                print(f"Module root found: {fullpath}")
                return fullpath
        
        raise FileNotFoundError(path)     
        
    
    def load_module(self, name: str, path: str, **kwargs):
        self.name = name
        self.path = path
        self.args = kwargs
        
        init_path = self.find_module_init(path)
        
        spec = importlib.util.spec_from_file_location(name, init_path)
        if spec is None:
            print_error(f"FATAL_ERROR: spec for module {name} at '{path}' could not be created.")
        

        spec.submodule_search_locations.append(os.path.dirname(path)) ## directory of file)
        self.loaded = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = self.loaded 
        spec.loader.exec_module(self.loaded)
        
        self.verify_module()
        
    def verify_module(self) -> bool:
        for i in self.required_attrs:
            if not hasattr(self.loaded, i):
                return False
        
        return True
        
    
    def inject_globals(self, host):
        setattr(self.loaded, 'settings', settings)
        setattr(self.loaded, 'host', host)
    
    def init(self):
        self.loaded.init(self.name, self.path, self.args)
        
        
from .api_proc_wrapper import ApiProcWrapper
from .db_wrapper import DatabaseWrapper
from .encryption_wrapper import EncryptionWrapper
from .server_wrapper import ServerWrapper
from .session_wrapper import SessionWrapper


class AZeroModuleHost:   
    api_proc: ApiProcWrapper
    db: DatabaseWrapper
    encryption: EncryptionWrapper
    server: ServerWrapper
    session: SessionWrapper

    def __init__(self) -> None:
        super().__init__()
        
        self.api_proc = ApiProcWrapper(self)
        self.db = DatabaseWrapper(self)
        self.encryption = EncryptionWrapper(self)
        self.server = ServerWrapper(self)
        self.session = SessionWrapper(self)
        
        # Initialize Modules:
        self.db.init()
        self.encryption.init()
        self.api_proc.init()
        self.server.init()
        self.session.init()
        
        
host: AZeroModuleHost = None
def create_host():
    global host
    host = AZeroModuleHost()