import os
from .template import Settings
from .rna_seq_pipeline import RNASeqPipeline


class Main:

    def main(
            self,
            ref_fa: str,
            gtf: str,
            fq1: str,
            fq2: str,
            adapter: str,
            base_quality_cutoff: int,
            min_read_length: int,
            read_aligner: str,
            bowtie2_mode: str,
            discard_bam: bool,
            min_count_mapq: int,
            nonunique_count: str,
            stranded_count: str,
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
            bowtie2_mode=bowtie2_mode,
            base_quality_cutoff=base_quality_cutoff,
            discard_bam=discard_bam,
            ref_fa=ref_fa,
            gtf=gtf)
