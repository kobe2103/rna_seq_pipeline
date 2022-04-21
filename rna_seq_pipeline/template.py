import subprocess
from datetime import datetime


class Settings:

    workdir: str
    outdir: str
    threads: int
    debug: bool

    def __init__(
            self,
            workdir: str,
            outdir: str,
            threads: int,
            debug: bool):

        self.workdir = workdir
        self.outdir = outdir
        self.threads = threads
        self.debug = debug


class Logger:

    INFO: str = 'INFO'
    DEBUG: str = 'DEBUG'

    name: str
    level: str

    def __init__(self, name: str, level: str):
        self.name = name
        assert level in [self.INFO, self.DEBUG]
        self.level = level

    def info(self, msg: str):
        print(f'{self.name}\tINFO\t{datetime.now()}', flush=True)
        print(msg + '\n', flush=True)

    def debug(self, msg: str):
        if self.level == self.INFO:
            return
        print(f'{self.name}\tDEBUG\t{datetime.now()}', flush=True)
        print(msg + '\n', flush=True)


class Processor:

    workdir: str
    outdir: str
    threads: int
    debug: bool
    settings: Settings

    def __init__(self, settings: Settings):
        self.workdir = settings.workdir
        self.outdir = settings.outdir
        self.threads = settings.threads
        self.debug = settings.debug
        self.settings = settings

        self.logger = Logger(
            name=self.__class__.__name__,
            level=Logger.DEBUG if self.debug else Logger.INFO
        )

    def call(self, cmd: str):
        self.logger.info(cmd)
        subprocess.check_call(cmd, shell=True)
