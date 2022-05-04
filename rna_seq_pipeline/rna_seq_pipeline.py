from .counting import HTSeq
from .mapping import Mapping
from .template import Processor
from .trimming import Cutadapt, FastQC


class RNASeqPipeline(Processor):

    ref_fa: str
    gtf: str
    fq1: str
    fq2: str
    adapter: str
    read_aligner: str

    trimmed_fq1: str
    trimmed_fq2: str
    sorted_bam: str
    count_csv: str

    def main(self,
             ref_fa: str,
             gtf: str,
             fq1: str,
             fq2: str,
             adapter: str,
             read_aligner: str):

        self.ref_fa = ref_fa
        self.gtf = gtf
        self.fq1 = fq1
        self.fq2 = fq2
        self.adapter = adapter
        self.read_aligner = read_aligner

        self.trimming()
        self.fastqc()
        self.mapping()
        self.counting()

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
            read_aligner=self.read_aligner)

    def counting(self):
        self.count_csv = HTSeq(self.settings).main(
            sorted_bam=self.sorted_bam,
            gtf=self.gtf)
