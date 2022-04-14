from .template import Settings, Processor
from .CONSTANT import *


class HTSeq(Processor):

    sorted_bam: str
    gtf: str
    out_counts: str

    def __init__(self, settings: Settings):
        super().__init__(settings=settings)

    def main(self,
             sorted_bam: str,
             gtf: str) -> str:

        self.sorted_bam = sorted_bam
        self.gtf = gtf

        self.set_output_path()
        self.htseq()

        return self.out_counts

    def set_output_path(self):
        self.out_counts = f'{self.outdir}/out_counts.csv'

    def htseq(self):
        cmd = f'htseq-count \
                --format bam \
                --order name \
                --stranded {STANDARD_SPECIFIC_ASSAY} \
                -a {SKIP_LOWER_QUALITY_READ} \
                --type exon \
                --idattr gene_id \
                --mode {MODE_TO_HANDLE_READ_OVERLAPPING} \
                {self.sorted_bam} \
                {self.gtf} \
                > {self.out_counts}'
        self.call(cmd)
