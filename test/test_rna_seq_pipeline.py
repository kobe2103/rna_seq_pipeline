from .setup import TestCase
from rna_seq_pipeline.rna_seq_pipeline import RNASeqPipeline


class TestRNASeqPipeline(TestCase):

    def setUp(self):
        self.set_up(py_path=__file__)

    def tearDown(self):
        self.tear_down()

    def test_main(self):
        RNASeqPipeline(self.settings).main(
            ref_fa=f'{self.indir}/21_0501_subset_mouse_genome.fa',
            gtf=f'{self.indir}/21_0501_subset_mouse_genome.gtf',
            fq1=f'{self.indir}/1month-4NQO-3.1.fq',
            fq2=f'{self.indir}/1month-4NQO-3.2.fq',
            adapter_fwd='AGATCGGAAGAGC',
            adapter_rev='AGATCGGAAGAGC'
        )
