from .template import Settings, Processor
from .trimming import Cutadapt, FastQC
from .mapping import Star
from .counting import HTSeq


class RNASeqPipeline(Processor):

    ref_fa: str
    gtf: str
    fq1: str
    fq2: str
    adapter_fwd: str
    adapter_rev: str

    trimmed_fq1: str
    trimmed_fq2: str
    sorted_bam: str
    count_csv: str

    def __init__(self, settings: Settings):
        super().__init__(settings=settings)

    def main(self,
             ref_fa: str,
             gtf: str,
             fq1: str,
             fq2: str,
             adapter_fwd: str,
             adapter_rev: str):

        self.ref_fa = ref_fa
        self.gtf = gtf
        self.fq1 = fq1
        self.fq2 = fq2
        self.adapter_fwd = adapter_fwd
        self.adapter_rev = adapter_rev

        self.trimming()
        self.fastqc()
        self.mapping()
        self.counting()

    def trimming(self):
        self.trimmed_fq1, self.trimmed_fq2 = Cutadapt(self.settings).main(
            fq1=self.fq1,
            fq2=self.fq2,
            adapter_fwd=self.adapter_fwd,
            adapter_rev=self.adapter_rev)

    def fastqc(self):
        FastQC(self.settings).main(
            trimmed_fq1=self.trimmed_fq1,
            trimmed_fq2=self.trimmed_fq2)

    def mapping(self):
        self.sorted_bam = Star(self.settings).main(
            ref_fa=self.ref_fa,
            gtf=self.gtf,
            trimmed_fq1=self.trimmed_fq1,
            trimmed_fq2=self.trimmed_fq2)

    def counting(self):
        self.count_csv = HTSeq(self.settings).main(
            sorted_bam=self.sorted_bam,
            gtf=self.gtf)
