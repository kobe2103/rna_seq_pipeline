from .setup import TestCase
from rna_seq_pipeline.mapping import Bowtie2, Star


class TestBowtie2(TestCase):

    def setUp(self):
        self.set_up(py_path=__file__)

    def tearDown(self):
        self.tear_down()

    def test_main(self):
        Bowtie2(self.settings).main(
            ref_fa=f'{self.indir}/21_0501_subset_mouse_genome.fa',
            fq1=f'{self.indir}/1month-4NQO-3.1.fq.gz',
            fq2=f'{self.indir}/1month-4NQO-3.2.fq.gz'
        )


class TestStar(TestCase):

    def setUp(self):
        self.set_up(py_path=__file__)

    def tearDown(self):
        self.tear_down()

    def test_main(self):
        Star(self.settings).main(
            ref_fa=f'{self.indir}/21_0501_subset_mouse_genome.fa',
            gtf=f'{self.indir}/21_0501_subset_mouse_genome.gtf',
            fq1=f'{self.indir}/trimmed_1.fq',
            fq2=f'{self.indir}/trimmed_2.fq',
        )
