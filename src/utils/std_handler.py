import sys
import io

from typing import List



custom_loggers = []
allowed_chars = """0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\\\'()*+,-./:;<=>?@[]^_`{|}~ \t\n"""

class CustomStdout:
    stream: str
    # old_stdout: io.TextIOWrapper
    substreams: List[io.TextIOWrapper]
    updated: bool

    def __init__(self, old_stdout = None, use_file = True):
        global custom_loggers
        self.level = "INFO"
        self.substreams = []
        self.updated = False
        self.old_stdout = old_stdout

        if old_stdout is not None:
            self.substreams.append(old_stdout)
        if use_file:
            self.substreams.append(open('out.log', 'w'))

        self.stream = ""
        self.stream_sanatized = ""
        custom_loggers.append(self)

    def write(self, data):
        self.stream += data
        for i in self.substreams:
            i.write(data)

        self.write_sanitized(data)
        self.updated = True

    def write_sanitized(self, data):
        global allowed_chars
        self.stream_sanatized += ''.join(filter(lambda x: x in allowed_chars, str(data)))

    def flush(self):
        for i in self.substreams:
            i.flush()

    def get_all(self):
        return self.stream

    def get_sanitized(self):
        return self.stream_sanatized



my_stdout = CustomStdout(sys.stdout)
def init():
    global my_stdout
    sys.stdout = my_stdout