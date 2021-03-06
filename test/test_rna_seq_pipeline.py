from .setup import TestCase
from rna_seq_pipeline.rna_seq_pipeline import RNASeqPipeline


class TestRNASeqPipeline(TestCase):

    def setUp(self):
        self.set_up(py_path=__file__)

    def tearDown(self):
        self.tear_down()

    def test_main(self):
        RNASeqPipeline(self.settings).main(
            ref_fa=f'{self.indir}/21_0501_subset_mouse_genome.fa.gz',
            gtf=f'{self.indir}/21_0501_subset_mouse_genome.gtf.gz',
            fq1=f'{self.indir}/1month-4NQO-3.1.fq.gz',
            fq2=f'{self.indir}/1month-4NQO-3.2.fq.gz',
            adapter='AGATCGGAAGAGC',
            base_quality_cutoff=20,
            min_read_length=20,
            max_read_length=None,
            read_aligner='star',
            bowtie2_mode='sensitive',
            discard_bam=False,
            min_count_mapq=10,
            nonunique_count='none',
            stranded_count='yes'
        )
