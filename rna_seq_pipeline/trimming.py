from typing import Tuple, Optional
from .template import Processor


class Trimming(Processor):

    fq1: str
    fq2: Optional[str]
    adapter: str
    base_quality_cutoff: int
    min_read_length: int
    max_read_length: Optional[int]

    trimmed_fq1: str
    trimmed_fq2: Optional[str]

    def main(self,
             fq1: str,
             fq2: Optional[str],
             adapter: str,
             base_quality_cutoff: int,
             min_read_length: int,
             max_read_length: Optional[int]) -> Tuple[str, Optional[str]]:

        self.fq1 = fq1
        self.fq2 = fq2
        self.adapter = adapter
        self.base_quality_cutoff = base_quality_cutoff
        self.min_read_length = min_read_length
        self.max_read_length = max_read_length

        if self.fq2 is not None:
            self.trimmed_fq1, self.trimmed_fq2 = CutadaptPairedEnd(self.settings).main(
                fq1=self.fq1,
                fq2=self.fq2,
                adapter=self.adapter,
                base_quality_cutoff=self.base_quality_cutoff,
                min_read_length=self.min_read_length,
                max_read_length=self.max_read_length)
        else:
            self.trimmed_fq1 = CutadaptSingleEnd(self.settings).main(
                fq=self.fq1,
                adapter=self.adapter,
                base_quality_cutoff=self.base_quality_cutoff,
                min_read_length=self.min_read_length,
                max_read_length=self.max_read_length)
            self.trimmed_fq2 = None

        return self.trimmed_fq1, self.trimmed_fq2


class CutadaptBase(Processor):

    MINIMUM_OVERLAP = 3
    MAXIMUM_ERROR_RATE = 0.1

    adapter: str
    base_quality_cutoff: int
    min_read_length: int
    max_read_length: Optional[int]


class CutadaptPairedEnd(CutadaptBase):

    fq1: str
    fq2: str

    trimmed_fq1: str
    trimmed_fq2: str

    def main(self,
             fq1: str,
             fq2: str,
             adapter: str,
             base_quality_cutoff: int,
             min_read_length: int,
             max_read_length: Optional[int]) -> Tuple[str, str]:

        self.fq1 = fq1
        self.fq2 = fq2
        self.adapter = adapter
        self.base_quality_cutoff = base_quality_cutoff
        self.min_read_length = min_read_length
        self.max_read_length = max_read_length

        self.set_output_paths()
        self.cutadapt()

        return self.trimmed_fq1, self.trimmed_fq2

    def set_output_paths(self):
        self.trimmed_fq1 = f'{self.workdir}/trimmed_1.fq'
        self.trimmed_fq2 = f'{self.workdir}/trimmed_2.fq'

    def cutadapt(self):
        lines = [
            'cutadapt',
            f'--adapter {self.adapter}',
            f'-A {self.adapter}',
            f'--overlap {self.MINIMUM_OVERLAP}',
            f'--error-rate {self.MAXIMUM_ERROR_RATE}',
            f'--quality-cutoff {self.base_quality_cutoff}',
            f'--output {self.trimmed_fq1}',
            f'--paired-output {self.trimmed_fq2}',
            f'--minimum-length {self.min_read_length}',
        ]
        if self.max_read_length is not None:
            lines.append(f'--maximum-length {self.max_read_length}')
        log = f'{self.outdir}/cutadapt.log'
        lines += [
            self.fq1,
            self.fq2,
            f'1> {log}',
            f'2> {log}',
        ]
        cmd = self.CMD_LINEBREAK.join(lines)
        self.call(cmd)


class CutadaptSingleEnd(CutadaptBase):

    fq: str

    trimmed_fq: str

    def main(self,
             fq: str,
             adapter: str,
             base_quality_cutoff: int,
             min_read_length: int,
             max_read_length: Optional[int]) -> str:

        self.fq = fq
        self.adapter = adapter
        self.base_quality_cutoff = base_quality_cutoff
        self.min_read_length = min_read_length
        self.max_read_length = max_read_length

        self.set_output_path()
        self.cutadapt()

        return self.trimmed_fq

    def set_output_path(self):
        self.trimmed_fq = f'{self.workdir}/trimmed.fq'

    def cutadapt(self):
        lines = [
            'cutadapt',
            f'--adapter {self.adapter}',
            f'--overlap {self.MINIMUM_OVERLAP}',
            f'--error-rate {self.MAXIMUM_ERROR_RATE}',
            f'--quality-cutoff {self.base_quality_cutoff}',
            f'--output {self.trimmed_fq}',
            f'--minimum-length {self.min_read_length}',
        ]
        if self.max_read_length is not None:
            lines.append(f'--maximum-length {self.max_read_length}')
        log = f'{self.outdir}/cutadapt.log'
        lines += [
            self.fq,
            f'1> {log}',
            f'2> {log}',
        ]
        cmd = self.CMD_LINEBREAK.join(lines)
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
        cmd = f'''fastqc \\
--outdir {self.outdir} \\
--threads {self.threads} \\
{self.fq1} {fq2} \\
1> {log} \\
2> {log}'''
        self.call(cmd)
