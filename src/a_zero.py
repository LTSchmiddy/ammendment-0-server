import sys
import multiprocessing
import time
import module_loader as ml

should_quit = False

def main():
    from utils import std_handler
    std_handler.init()

    if sys.platform.startswith("win"):
        # On Windows calling this function is necessary for freezing.
        multiprocessing.freeze_support()

    import settings.paths
    settings.load_settings()

    ml.create_host()
    ml.host.server.start_server()
    

if __name__ == "__main__":
    main()