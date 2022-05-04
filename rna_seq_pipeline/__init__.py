import os
from .rna_seq_pipeline import RNASeqPipeline
from .template import Settings


class Main:

    def main(
            self,
            ref_fa: str,
            gtf: str,
            fq1: str,
            fq2: str,
            adapter: str,
            read_aligner: str,
            discard_bam: bool,
            outdir: str,
            threads: str,
            debug: bool):

        workdir = 'rna_seq_pipeline_workdir'

        settings = Settings(
            workdir=workdir,
            outdir=outdir,
            threads=int(threads),
            debug=debug)

        for d in [settings.workdir, settings.outdir]:
            os.makedirs(d, exist_ok=True)

        RNASeqPipeline(settings).main(
            fq1=fq1,
            fq2=fq2 if fq2 != 'None' else None,
            adapter=adapter,
            read_aligner=read_aligner,
            discard_bam=discard_bam,
            ref_fa=ref_fa,
            gtf=gtf)
