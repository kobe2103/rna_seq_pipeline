from typing import Optional
from .mapping import Mapping
from .clean_up import CleanUp
from .counting import Counting
from .template import Processor
from .trimming import Cutadapt, FastQC
from .copy_ref_files import CopyRefFiles


class RNASeqPipeline(Processor):

    ref_fa: str
    gtf: str
    fq1: str
    fq2: Optional[str]
    adapter: str
    read_aligner: str
    discard_bam: bool

    trimmed_fq1: str
    trimmed_fq2: Optional[str]
    sorted_bam: str
    count_csv: str

    def main(self,
             ref_fa: str,
             gtf: str,
             fq1: str,
             fq2: Optional[str],
             adapter: str,
             read_aligner: str,
             discard_bam: bool):

        self.ref_fa = ref_fa
        self.gtf = gtf
        self.fq1 = fq1
        self.fq2 = fq2
        self.adapter = adapter
        self.read_aligner = read_aligner
        self.discard_bam = discard_bam

        self.copy_ref_files()
        self.trimming()
        self.fastqc()
        self.mapping()
        self.counting()
        self.clean_up()

    def copy_ref_files(self):
        self.ref_fa, self.gtf = CopyRefFiles(self.settings).main(
            ref_fa=self.ref_fa, gtf=self.gtf)

    def trimming(self):
        self.trimmed_fq1, self.trimmed_fq2 = Cutadapt(self.settings).main(
            fq1=self.fq1,
            fq2=self.fq2,
            adapter=self.adapter)

    def fastqc(self):
        FastQC(self.settings).main(
            fq1=self.trimmed_fq1,
            fq2=self.trimmed_fq2)

    def mapping(self):
        self.sorted_bam = Mapping(self.settings).main(
            ref_fa=self.ref_fa,
            gtf=self.gtf,
            fq1=self.trimmed_fq1,
            fq2=self.trimmed_fq2,
            read_aligner=self.read_aligner,
            discard_bam=self.discard_bam)

    def counting(self):
        self.count_csv = Counting(self.settings).main(
            sorted_bam=self.sorted_bam,
            gtf=self.gtf)

    def clean_up(self):
        CleanUp(self.settings).main()
