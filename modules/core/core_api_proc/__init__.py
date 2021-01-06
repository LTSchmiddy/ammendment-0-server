import os
import sys
import base64
from typing import Union

settings = None

from . import commands

class ApiHandler:
    cmds: dict
    
    def __init__(self):
        self.cmds = {}
        
        for i in commands.CommandBase.__subclasses__():
            self.cmds[i.cmd] = i
            print(f"Command Loaded: {i.cmd} {i}")
    
    def run_command(self, cmd: str, user_id: str, mac_addr: str, token: Union[str, None], args=Union[dict, None]):
        if not cmd in self.cmds:
            pass
                
        return self.cmds[cmd].run_command(user_id, mac_addr, token, args)



a_handler: ApiHandler = None
def init(name: str, path: str, args: dict[str, str]):
    global a_handler
    a_handler = ApiHandler()


def run_command(cmd: str, user_id: str, mac_addr: str, token: Union[str, None], args=Union[dict, None]):
    global a_handler
    return a_handler.run_command(cmd, user_id, mac_addr, token, args)
    