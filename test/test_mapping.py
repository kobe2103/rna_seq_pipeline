from .setup import TestCase
from rna_seq_pipeline.mapping import Bowtie2, Star


class TestBowtie2(TestCase):

    def setUp(self):
        self.set_up(py_path=__file__)

    def tearDown(self):
        self.tear_down()

    def test_main(self):
        Bowtie2(self.settings).main(
            ref_fa=f'{self.indir}/NC_045512.2.fa',
            trimmed_fq1=f'{self.outdir}/R1.fastq',
            trimmed_fq2=f'{self.outdir}/R2.fastq'
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
            trimmed_fq1=f'{self.indir}/trimmed_1.fq',
            trimmed_fq2=f'{self.indir}/trimmed_2.fq',
        )
