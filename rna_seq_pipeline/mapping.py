import os
from .template import Processor, Settings
from .CONSTANT import *


class Bowtie2(Processor):

    ref_fa: str
    trimmed_fq1: str
    trimmed_fq2: str

    idx: str
    sam: str
    bam: str
    sorted_bam: str

    def __init__(self, settings: Settings):
        super().__init__(settings=settings)

    def main(
            self,
            ref_fa: str,
            trimmed_fq1: str,
            trimmed_fq2: str) -> str:

        self.ref_fa = ref_fa
        self.trimmed_fq1 = trimmed_fq1
        self.trimmed_fq2 = trimmed_fq2

        self.indexing()
        self.mapping()
        self.sam_to_bam()
        self.sort_bam()

        return self.sorted_bam

    def indexing(self):
        self.idx = f'{self.workdir}/bowtie2-index'
        cmd = f'bowtie2-build {self.ref_fa} {self.idx}'
        self.call(cmd)

    def set_file_path(self):
        self.sam = f'{self.outdir}/mapped.sam'
        self.bam = f'{self.outdir}/mapped.bam'
        self.sorted_bam = f'{self.outdir}/sorted.bam'

    def mapping(self):
        cmd = f'bowtie2 \
                        -x {self.idx} \
                        -1 {self.trimmed_fq1} \
                        -2 {self.trimmed_fq2} \
                        -S {self.sam}'
        self.call(cmd)

    def sam_to_bam(self):
        cmd = f'samtools view -b -h {self.sam} > {self.bam}'
        self.call(cmd)

    def sort_bam(self):
        cmd = f'samtools sort {self.bam} > {self.sorted_bam}'
        self.call(cmd)


class Star(Processor):

    ref_fa: str
    gtf: str
    trimmed_fq1: str
    trimmed_fq2: str

    genome_dir: str
    mapping_out_prefix: str

    def __init__(self, settings: Settings):
        super().__init__(settings=settings)

    def main(
            self,
            ref_fa: str,
            gtf: str,
            trimmed_fq1: str,
            trimmed_fq2: str) -> str:

        self.ref_fa = ref_fa
        self.gtf = gtf
        self.trimmed_fq1 = trimmed_fq1
        self.trimmed_fq2 = trimmed_fq2

        self.indexing()
        self.mapping()

        return f'{self.mapping_out_prefix}{MAPPING_OUT_SUFFIX}'

    def indexing(self):
        self.genome_dir = f'{self.workdir}/genomeDir'
        os.makedirs(self.genome_dir, exist_ok=True)
        cmd = f'STAR \
                --runThreadN {self.threads} \
                --runMode genomeGenerate \
                --genomeDir {self.genome_dir} \
                --genomeFastaFiles {self.ref_fa} \
                --sjdbGTFfile {self.gtf} \
                --sjdbOverhang {LENGTH_OF_DONOR_SEQUENCE} \
                --outFileNamePrefix {self.workdir}/STAR'
        self.call(cmd)

    def mapping(self):
        self.mapping_out_prefix = f'{self.outdir}/STAR_mapping_'
        cmd = f'STAR \
                --genomeDir {self.genome_dir} \
                --runThreadN {self.threads} \
                --readFilesIn {self.trimmed_fq1} {self.trimmed_fq2} \
                --outSAMtype {OUT_SAM_TYPE} \
                --outFileNamePrefix {self.mapping_out_prefix} \
                --outSAMunmapped None \
                --outSAMattributes {SAM_ATTIRBUTE}'
        self.call(cmd)
