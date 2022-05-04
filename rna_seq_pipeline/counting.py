from .template import Processor


class HTSeq(Processor):

    STANDARD_SPECIFIC_ASSAY = 'yes'
    SKIP_LOWER_QUALITY_READ = '10'
    MODE_TO_HANDLE_READ_OVERLAPPING = 'union'
    GENE_ID_COLUMN = 'gene_id'
    COUNT_COLUMN = 'count'

    sorted_bam: str
    gtf: str

    htseq_txt: str
    count_tsv: str
    remaining_count_txt: str

    def main(self,
             sorted_bam: str,
             gtf: str) -> str:
        self.sorted_bam = sorted_bam
        self.gtf = gtf

        self.index_bam()
        self.htseq()
        self.write_count_tsv()
        self.write_remaining_count_txt()

        return self.count_tsv

    def index_bam(self):
        self.call(f'samtools index {self.sorted_bam}')

    def htseq(self):
        self.htseq_txt = f'{self.workdir}/counts.txt'
        log = f'{self.outdir}/htseq-count.log'
        cmd = f'''htseq-count \\
--format bam \\
--order name \\
--stranded {self.STANDARD_SPECIFIC_ASSAY} \\
-a {self.SKIP_LOWER_QUALITY_READ} \\
--type exon \\
--idattr gene_id \\
--mode {self.MODE_TO_HANDLE_READ_OVERLAPPING} \\
{self.sorted_bam} \\
{self.gtf} \\
1> {self.htseq_txt} \\
2> {log}'''
        self.call(cmd)

    def write_count_tsv(self):
        self.count_tsv = f'{self.outdir}/counts.tsv'
        with open(self.count_tsv, 'w') as writer:
            header_line = f'{self.GENE_ID_COLUMN}\t{self.COUNT_COLUMN}\n'
            writer.write(header_line)
            with open(self.htseq_txt) as reader:
                for line in reader:
                    if not line.startswith('__'):
                        writer.write(line)

    def write_remaining_count_txt(self):
        self.remaining_count_txt = f'{self.outdir}/remaining-counts.txt'
        with open(self.remaining_count_txt, 'w') as writer:
            with open(self.htseq_txt) as reader:
                for line in reader:
                    if line.startswith('__'):
                        writer.write(line)
