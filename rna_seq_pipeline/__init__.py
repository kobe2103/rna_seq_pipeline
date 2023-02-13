import os
from .template import Settings
from .tools import get_temp_path
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
            max_read_length: int,
            read_aligner: str,
            bowtie2_mode: str,
            discard_bam: bool,
            min_count_mapq: int,
            nonunique_count: str,
            stranded_count: str,
            outdir: str,
            threads: int,
            debug: bool):

        workdir = get_temp_path('rna_seq_pipeline_workdir_')

        settings = Settings(
            workdir=workdir,
            outdir=outdir,
            threads=threads,
            debug=debug)

        for d in [settings.workdir, settings.outdir]:
            os.makedirs(d, exist_ok=True)

        RNASeqPipeline(settings).main(
            fq1=fq1,
            fq2=None if fq2.lower() == 'none' else fq2,
            adapter=adapter,
            base_quality_cutoff=base_quality_cutoff,
            min_read_length=min_read_length,
            max_read_length=None if max_read_length == -1 else max_read_length,
            read_aligner=read_aligner,
            bowtie2_mode=bowtie2_mode,
            discard_bam=discard_bam,
            min_count_mapq=min_count_mapq,
            nonunique_count=nonunique_count,
            stranded_count=stranded_count,
            ref_fa=ref_fa,
            gtf=gtf)
