import os
from .constant import *
from .template import Processor


class Bowtie2(Processor):

    ref_fa: str
    fq1: str
    fq2: str

    idx: str
    sam: str
    bam: str
    sorted_bam: str

    def main(
            self,
            ref_fa: str,
            fq1: str,
            fq2: str) -> str:

        self.ref_fa = ref_fa
        self.fq1 = fq1
        self.fq2 = fq2

        self.indexing()
        self.mapping()
        self.sam_to_bam()
        self.sort_bam()

        return self.sorted_bam

    def indexing(self):
        self.idx = f'{self.workdir}/bowtie2-index'
        log = f'{self.outdir}/bowtie2-build.log'
        self.call(f'bowtie2-build {self.ref_fa} {self.idx} 1> {log} 2> {log}')

    def mapping(self):
        log = f'{self.outdir}/bowtie2.log'
        self.sam = f'{self.workdir}/mapped.sam'
        cmd = f'''bowtie2 \
                  -x {self.idx} \
                  -1 {self.fq1} \
                  -2 {self.fq2} \
                  -S {self.sam} \
                  1> {log} \
                  2> {log}'''
        self.call(cmd)

    def sam_to_bam(self):
        self.bam = f'{self.workdir}/mapped.bam'
        self.call(f'samtools view -b -h {self.sam} > {self.bam}')

    def sort_bam(self):
        self.sorted_bam = f'{self.outdir}/sorted.bam'
        self.call(f'samtools sort {self.bam} > {self.sorted_bam}')


class Star(Processor):

    ref_fa: str
    gtf: str
    fq1: str
    fq2: str

    genome_dir: str
    mapping_out_prefix: str

    def main(
            self,
            ref_fa: str,
            gtf: str,
            fq1: str,
            fq2: str) -> str:

        self.ref_fa = ref_fa
        self.gtf = gtf
        self.fq1 = fq1
        self.fq2 = fq2

        self.indexing()
        self.mapping()

        return f'{self.mapping_out_prefix}{MAPPING_OUT_SUFFIX}'

    def indexing(self):
        self.genome_dir = f'{self.workdir}/genomeDir'
        os.makedirs(self.genome_dir, exist_ok=True)
        log = f'{self.outdir}/STAR-genomeGenerate.log'
        cmd = f'''STAR \
                  --runThreadN {self.threads} \
                  --runMode genomeGenerate \
                  --genomeDir {self.genome_dir} \
                  --genomeFastaFiles {self.ref_fa} \
                  --sjdbGTFfile {self.gtf} \
                  --sjdbOverhang {LENGTH_OF_DONOR_SEQUENCE} \
                  --outFileNamePrefix {self.workdir}/STAR \
                  1> {log} \
                  2> {log}'''
        self.call(cmd)

    def mapping(self):
        self.mapping_out_prefix = f'{self.outdir}/STAR_mapping_'
        cmd = f'''STAR \
                  --genomeDir {self.genome_dir} \
                  --runThreadN {self.threads} \
                  --readFilesIn {self.fq1} {self.fq2} \
                  --outSAMtype {OUT_SAM_TYPE} \
                  --outFileNamePrefix {self.mapping_out_prefix} \
                  --outSAMunmapped None \
                  --outSAMattributes {SAM_ATTRIBUTE}'''
        self.call(cmd)
