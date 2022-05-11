from typing import Optional
from .mapping import Mapping
from .clean_up import CleanUp
from .counting import Counting
from .template import Processor
from .trimming import Trimming, FastQC
from .copy_ref_files import CopyRefFiles


class RNASeqPipeline(Processor):

    ref_fa: str
    gtf: str
    fq1: str
    fq2: Optional[str]
    adapter: str
    base_quality_cutoff: int
    min_read_length: int
    max_read_length: Optional[int]
    read_aligner: str
    bowtie2_mode: str
    discard_bam: bool
    min_count_mapq: int
    nonunique_count: str
    stranded_count: str

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
             base_quality_cutoff: int,
             min_read_length: int,
             max_read_length: Optional[int],
             read_aligner: str,
             bowtie2_mode: str,
             discard_bam: bool,
             min_count_mapq: int,
             nonunique_count: str,
             stranded_count: str):

        self.ref_fa = ref_fa
        self.gtf = gtf
        self.fq1 = fq1
        self.fq2 = fq2
        self.adapter = adapter
        self.base_quality_cutoff = base_quality_cutoff
        self.min_read_length = min_read_length
        self.max_read_length = max_read_length
        self.read_aligner = read_aligner
        self.bowtie2_mode = bowtie2_mode
        self.discard_bam = discard_bam
        self.min_count_mapq = min_count_mapq
        self.nonunique_count = nonunique_count
        self.stranded_count = stranded_count

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
        self.trimmed_fq1, self.trimmed_fq2 = Trimming(self.settings).main(
            fq1=self.fq1,
            fq2=self.fq2,
            adapter=self.adapter,
            base_quality_cutoff=self.base_quality_cutoff,
            min_read_length=self.min_read_length,
            max_read_length=self.max_read_length)

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
            bowtie2_mode=self.bowtie2_mode,
            discard_bam=self.discard_bam)

    def counting(self):
        self.count_csv = Counting(self.settings).main(
            sorted_bam=self.sorted_bam,
            gtf=self.gtf,
            min_count_mapq=self.min_count_mapq,
            nonunique_count=self.nonunique_count,
            stranded_count=self.stranded_count,
        )

    def clean_up(self):
        CleanUp(self.settings).main()
