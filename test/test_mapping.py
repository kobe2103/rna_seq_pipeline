from .setup import TestCase
from rna_seq_pipeline.mapping import Bowtie2, Star, Mapping


class TestMapping(TestCase):

    def setUp(self):
        self.set_up(py_path=__file__)

    def tearDown(self):
        self.tear_down()

    def test_paired_end(self):
        actual = Mapping(self.settings).main(
            ref_fa=f'{self.indir}/21_0501_subset_mouse_genome.fa',
            gtf=f'{self.indir}/21_0501_subset_mouse_genome.gtf',
            fq1=f'{self.indir}/trimmed_1.fq',
            fq2=f'{self.indir}/trimmed_2.fq',
            read_aligner='STAR',
            discard_bam=True
        )
        expected = f'{self.workdir}/sorted.bam'
        self.assertFileExists(expected, actual)

    def test_single_end(self):
        actual = Mapping(self.settings).main(
            ref_fa=f'{self.indir}/21_0501_subset_mouse_genome.fa',
            gtf=f'{self.indir}/21_0501_subset_mouse_genome.gtf',
            fq1=f'{self.indir}/trimmed_1.fq',
            fq2=None,
            read_aligner='STAR',
            discard_bam=True
        )
        expected = f'{self.workdir}/sorted.bam'
        self.assertFileExists(expected, actual)


class TestBowtie2(TestCase):

    def setUp(self):
        self.set_up(py_path=__file__)

    def tearDown(self):
        self.tear_down()

    def test_paired_end(self):
        Bowtie2(self.settings).main(
            ref_fa=f'{self.indir}/21_0501_subset_mouse_genome.fa',
            fq1=f'{self.indir}/trimmed_1.fq',
            fq2=f'{self.indir}/trimmed_2.fq'
        )

    def test_single_end(self):
        Bowtie2(self.settings).main(
            ref_fa=f'{self.indir}/21_0501_subset_mouse_genome.fa',
            fq1=f'{self.indir}/trimmed_1.fq',
            fq2=None
        )


class TestStar(TestCase):

    def setUp(self):
        self.set_up(py_path=__file__)

    def tearDown(self):
        self.tear_down()

    def test_paired_end(self):
        Star(self.settings).main(
            ref_fa=f'{self.indir}/21_0501_subset_mouse_genome.fa',
            gtf=f'{self.indir}/21_0501_subset_mouse_genome.gtf',
            fq1=f'{self.indir}/trimmed_1.fq',
            fq2=f'{self.indir}/trimmed_2.fq',
        )

    def test_single_end(self):
        Star(self.settings).main(
            ref_fa=f'{self.indir}/21_0501_subset_mouse_genome.fa',
            gtf=f'{self.indir}/21_0501_subset_mouse_genome.gtf',
            fq1=f'{self.indir}/trimmed_1.fq',
            fq2=None,
        )
