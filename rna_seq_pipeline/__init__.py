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
            fq2=fq2,
            adapter_fwd=adapter,
            adapter_rev=adapter,
            ref_fa=ref_fa,
            gtf=gtf)
