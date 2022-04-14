from .template import Settings, Processor
from .CONSTANT import *
from typing import Tuple


class Cutadapt(Processor):

    fq1: str
    fq2: str
    adapter_fwd: str
    adapter_rev: str
    trimmed_fq1: str
    trimmed_fq2: str

    def __init__(self, settings: Settings):
        super().__init__(settings=settings)

    def main(self,
             fq1: str,
             fq2: str,
             adapter_fwd: str,
             adapter_rev: str) -> Tuple[str, str]:

        self.fq1 = fq1
        self.fq2 = fq2
        self.adapter_fwd = adapter_fwd
        self.adapter_rev = adapter_rev

        self.set_output_paths()
        self.cutadapt()

        return self.trimmed_fq1, self.trimmed_fq2

    def set_output_paths(self):
        self.trimmed_fq1 = f'{self.outdir}/trimmed_1.fq'
        self.trimmed_fq2 = f'{self.outdir}/trimmed_2.fq'

    def cutadapt(self):
        cmd = f'cutadapt \
                --adapter {self.adapter_fwd} \
                -A {self.adapter_rev} \
                --overlap {MINIMUM_OVERLAP} \
                --error-rate {MAXIMUM_ERROR_RATE} \
                --minimum-length {MINIMUM_LENGTH} \
                --output {self.trimmed_fq1} \
                --paired-output {self.trimmed_fq2} \
                {self.fq1} \
                {self.fq2}'
        self.call(cmd)


class FastQC(Processor):

    trimmed_fq1: str
    trimmed_fq2: str

    def __init__(self, settings: Settings):
        super().__init__(settings=settings)

    def main(self,
             trimmed_fq1: str,
             trimmed_fq2: str):

        self.trimmed_fq1 = trimmed_fq1
        self.trimmed_fq2 = trimmed_fq2

        self.fastqc()

    def fastqc(self):
        cmd = f'fastqc \
                --outdir {self.outdir} \
                {self.trimmed_fq1} {self.trimmed_fq2} \
                --threads {self.threads}'
        self.call(cmd)
