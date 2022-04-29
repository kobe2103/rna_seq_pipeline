import os
from .template import Processor


class Mapping(Processor):

    ref_fa: str
    gtf: str
    fq1: str
    fq2: str
    read_aligner: str

    sorted_bam: str

    def main(
            self,
            ref_fa: str,
            gtf: str,
            fq1: str,
            fq2: str,
            read_aligner: str) -> str:

        self.ref_fa = ref_fa
        self.gtf = gtf
        self.fq1 = fq1
        self.fq2 = fq2
        self.read_aligner = read_aligner.lower()

        assert self.read_aligner in ['star', 'bowtie2']

        if self.read_aligner == 'star':
            self.run_star()
        else:
            self.run_bowtie2()

        return self.sorted_bam

    def run_star(self):
        self.sorted_bam = Star(self.settings).main(
            ref_fa=self.ref_fa,
            gtf=self.gtf,
            fq1=self.fq1,
            fq2=self.fq2)

    def run_bowtie2(self):
        self.sorted_bam = Bowtie2(self.settings).main(
            ref_fa=self.ref_fa,
            fq1=self.fq1,
            fq2=self.fq2)


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

    MAPPING_OUT_SUFFIX = 'Aligned.sortedByCoord.out.bam'  # given by STAR
    OUT_SAM_TYPE = 'BAM SortedByCoordinate'
    LENGTH_OF_DONOR_SEQUENCE = '100'
    SAM_ATTRIBUTES = 'Standard'

    ref_fa: str
    gtf: str
    fq1: str
    fq2: str

    genome_dir: str
    mapping_out_prefix: str
    sorted_bam: str

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
        self.rename_bam()

        return self.sorted_bam

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
                  --sjdbOverhang {self.LENGTH_OF_DONOR_SEQUENCE} \
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
                  --outSAMtype {self.OUT_SAM_TYPE} \
                  --outFileNamePrefix {self.mapping_out_prefix} \
                  --outSAMunmapped None \
                  --outSAMattributes {self.SAM_ATTRIBUTES}'''
        self.call(cmd)

    def rename_bam(self):
        src = f'{self.mapping_out_prefix}{self.MAPPING_OUT_SUFFIX}'
        self.sorted_bam = f'{self.outdir}/sorted.bam'
        self.call(f'mv {src} {self.sorted_bam}')
