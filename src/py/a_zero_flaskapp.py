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


    return server.flask_site.app

app = construct_app()
