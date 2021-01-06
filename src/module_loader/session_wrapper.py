from . import AZeroModuleWrapper

class SessionWrapper(AZeroModuleWrapper):
    module_type = "session"
    
    required_methods = [
        'init',
        'start_server',
        'stop_server',
        'get_addr'
    ]
    
    def verify_module(self) -> bool:
        if not super().verify_module():
            return False
        
        return True
    
    def start_server(self):
        self.loaded.start_server()
        
    def stop_server(self):
        self.loaded.stop_server()
        
    def get_addr(self, path=""):
        return self.loaded.get_addr(path)