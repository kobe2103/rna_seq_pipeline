import subprocess


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

    def call(self, cmd: str):
        print(f'CMD: {cmd}', flush=True)
        subprocess.check_call(cmd, shell=True)
