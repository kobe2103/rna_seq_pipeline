from .setup import TestCase
from rna_seq_pipeline.mapping import Bowtie2, Star, Mapping


class TestMapping(TestCase):

    def setUp(self):
        self.set_up(py_path=__file__)

    def tearDown(self):
        self.tear_down()

    def test_main(self):
        actual = Mapping(self.settings).main(
            ref_fa=f'{self.indir}/21_0501_subset_mouse_genome.fa',
            gtf=f'{self.indir}/21_0501_subset_mouse_genome.gtf',
            fq1=f'{self.indir}/trimmed_1.fq',
            fq2=f'{self.indir}/trimmed_2.fq',
            read_aligner='STAR'
        )
        expected = f'{self.outdir}/sorted.bam'
        self.assertFileExists(expected, actual)


class TestBowtie2(TestCase):

    def setUp(self):
        self.set_up(py_path=__file__)

    def tearDown(self):
        self.tear_down()

    def test_main(self):
        Bowtie2(self.settings).main(
            ref_fa=f'{self.indir}/21_0501_subset_mouse_genome.fa',
            fq1=f'{self.indir}/trimmed_1.fq',
            fq2=f'{self.indir}/trimmed_2.fq'
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
