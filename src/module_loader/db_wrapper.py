from . import AZeroModuleWrapper

class DatabaseWrapper(AZeroModuleWrapper):
    module_type = "db"
    
    required_methods = [
        'init',
    ]
    
    def verify_module(self) -> bool:
        if not super().verify_module():
            return False
        
        return True
    
    