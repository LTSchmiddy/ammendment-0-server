import sys
import multiprocessing
import time

ordinal = lambda n: "%d%s" % (n, "tsnrhtdd"[(n // 10 % 10 != 1) * (n % 10 < 4) * n % 10::4])

should_quit = False

def construct_app():
    from utils import std_handler
    std_handler.init()

    if sys.platform.startswith("win"):
        # On Windows calling this function is necessary.
        multiprocessing.freeze_support()

    import settings.paths
    settings.load_settings()


    import server
    import db
    db.init()

    server.init()
    server.start_server()

    while not should_quit:
        time.sleep(1)

    server.stop_server()
    settings.save_settings()

    sys.exit(0)