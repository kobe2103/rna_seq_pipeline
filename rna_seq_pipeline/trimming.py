from typing import Tuple
from .template import Processor


class Cutadapt(Processor):

    MINIMUM_OVERLAP = '3'
    MAXIMUM_ERROR_RATE = '0.1'
    MINIMUM_LENGTH = '50'

    fq1: str
    fq2: str
    adapter: str
    trimmed_fq1: str
    trimmed_fq2: str

    def main(self,
             fq1: str,
             fq2: str,
             adapter: str) -> Tuple[str, str]:

        self.fq1 = fq1
        self.fq2 = fq2
        self.adapter = adapter

        self.set_output_paths()
        self.cutadapt()

        return self.trimmed_fq1, self.trimmed_fq2

    def set_output_paths(self):
        self.trimmed_fq1 = f'{self.outdir}/trimmed_1.fq'
        self.trimmed_fq2 = f'{self.outdir}/trimmed_2.fq'

    def cutadapt(self):
        log = f'{self.outdir}/cutadapt.log'
        cmd = f'''cutadapt \
                  --adapter {self.adapter} \
                  -A {self.adapter} \
                  --overlap {self.MINIMUM_OVERLAP} \
                  --error-rate {self.MAXIMUM_ERROR_RATE} \
                  --minimum-length {self.MINIMUM_LENGTH} \
                  --output {self.trimmed_fq1} \
                  --paired-output {self.trimmed_fq2} \
                  {self.fq1} \
                  {self.fq2} \
                  1> {log} \
                  2> {log}'''
        self.call(cmd)


class FastQC(Processor):

    fq1: str
    fq2: str

    def main(self,
             fq1: str,
             fq2: str):

        self.fq1 = fq1
        self.fq2 = fq2

        self.fastqc()

    def fastqc(self):
        cmd = f'fastqc \
                --outdir {self.outdir} \
                {self.fq1} {self.fq2} \
                --threads {self.threads}'
        self.call(cmd)
