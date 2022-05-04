from typing import Tuple, Optional
from .template import Processor


class Cutadapt(Processor):

    fq1: str
    fq2: Optional[str]
    adapter: str
    trimmed_fq1: str
    trimmed_fq2: Optional[str]

    def main(self,
             fq1: str,
             fq2: Optional[str],
             adapter: str) -> Tuple[str, Optional[str]]:

        self.fq1 = fq1
        self.fq2 = fq2
        self.adapter = adapter

        if self.fq2 is not None:
            self.trimmed_fq1, self.trimmed_fq2 = CutadaptPairedEnd(self.settings).main(
                fq1=self.fq1,
                fq2=self.fq2,
                adapter=self.adapter)
        else:
            self.trimmed_fq1 = CutadaptSingleEnd(self.settings).main(
                fq=self.fq1,
                adapter=self.adapter)
            self.trimmed_fq2 = None

        return self.trimmed_fq1, self.trimmed_fq2


class CutadaptBase(Processor):

    MINIMUM_OVERLAP = '3'
    MAXIMUM_ERROR_RATE = '0.1'
    MINIMUM_LENGTH = '50'


class CutadaptPairedEnd(CutadaptBase):

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
        self.trimmed_fq1 = f'{self.workdir}/trimmed_1.fq'
        self.trimmed_fq2 = f'{self.workdir}/trimmed_2.fq'

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


class CutadaptSingleEnd(CutadaptBase):

    fq: str
    adapter: str

    trimmed_fq: str

    def main(self,
             fq: str,
             adapter: str) -> str:

        self.fq = fq
        self.adapter = adapter

        self.set_output_path()
        self.cutadapt()

        return self.trimmed_fq

    def set_output_path(self):
        self.trimmed_fq = f'{self.workdir}/trimmed.fq'

    def cutadapt(self):
        log = f'{self.outdir}/cutadapt.log'
        cmd = f'''cutadapt \
                  --adapter {self.adapter} \
                  --overlap {self.MINIMUM_OVERLAP} \
                  --error-rate {self.MAXIMUM_ERROR_RATE} \
                  --minimum-length {self.MINIMUM_LENGTH} \
                  --output {self.trimmed_fq} \
                  {self.fq} \
                  1> {log} \
                  2> {log}'''
        self.call(cmd)


class FastQC(Processor):

    fq1: str
    fq2: Optional[str]

    def main(self,
             fq1: str,
             fq2: Optional[str]):

        self.fq1 = fq1
        self.fq2 = fq2

        self.fastqc()

    def fastqc(self):
        log = f'{self.outdir}/fastqc.log'
        fq2 = '' if self.fq2 is None else self.fq2
        cmd = f'''fastqc \
                  --outdir {self.outdir} \
                  --threads {self.threads} \
                  {self.fq1} {fq2} \
                  1> {log} 2> {log}'''
        self.call(cmd)
