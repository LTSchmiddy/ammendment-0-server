class CommandBase:
    cmd: str = "cmd_name"

    @staticmethod
    def run_command(user_id: str, mac_addr: str, token: str=None, args=None):
        pass


class ReturnMessageCommand(CommandBase):
    cmd: str = "return_message"

    @staticmethod
    def run_command(user_id: str, mac_addr: str, token: str=None, args=None):
        # print(args)
        return args




from .register_user import RegisterUserCommand