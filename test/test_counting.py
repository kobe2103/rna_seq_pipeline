from .setup import TestCase
from rna_seq_pipeline.counting import HTSeq


class TestHTSeq(TestCase):

    def setUp(self):
        self.set_up(py_path=__file__)

    def tearDown(self):
        self.tear_down()

    def test_main(self):
        HTSeq(self.settings).main(
            sorted_bam=f'{self.indir}/STAR_mapping_Aligned.sortedByCoord.out.bam',
            gtf=f'{self.indir}/21_0501_subset_mouse_genome.gtf'
        )
