from .setup import TestCase
from rna_seq_pipeline.counting import HTSeq


class TestHTSeq(TestCase):

    def setUp(self):
        self.set_up(py_path=__file__)

    def tearDown(self):
        self.tear_down()

    def test_main(self):
        actual = HTSeq(self.settings).main(
            sorted_bam=f'{self.indir}/sorted.bam',
            gtf=f'{self.indir}/21_0501_subset_mouse_genome.gtf'
        )
        expected = f'{self.outdir}/counts.tsv'
        self.assertFileExists(expected, actual)
