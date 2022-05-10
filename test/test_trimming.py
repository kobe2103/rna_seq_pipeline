from .setup import TestCase
from rna_seq_pipeline.trimming import FastQC, Trimming


class TestTrimming(TestCase):

    def setUp(self):
        self.set_up(py_path=__file__)

    def tearDown(self):
        self.tear_down()

    def test_paired_end(self):
        # https://sapac.support.illumina.com/bulletins/2016/12/what-sequences-do-i-use-for-adapter-trimming.html
        # 'AGATCGGAAGAGC' is the 'stem' of the Y-shaped adapter, i.e. the universal adapter sequence
        # read 1 and read 2's adapter sequence should be palindromic, thus fwd and rev should be the same
        fq1, fq2 = Trimming(self.settings).main(
            fq1=f'{self.indir}/1month-4NQO-3.1.fq.gz',
            fq2=f'{self.indir}/1month-4NQO-3.2.fq.gz',
            adapter='AGATCGGAAGAGC',
            base_quality_cutoff=20,
            min_read_length=20,
        )
        self.assertFileExists(f'{self.workdir}/trimmed_1.fq', fq1)
        self.assertFileExists(f'{self.workdir}/trimmed_2.fq', fq2)

    def test_single_end(self):
        fq1, fq2 = Trimming(self.settings).main(
            fq1=f'{self.indir}/1month-4NQO-3.1.fq.gz',
            fq2=None,
            adapter='AGATCGGAAGAGC',
            base_quality_cutoff=20,
            min_read_length=20,
        )
        self.assertFileExists(f'{self.workdir}/trimmed.fq', fq1)


class TestFastQC(TestCase):

    def setUp(self):
        self.set_up(py_path=__file__)

    def tearDown(self):
        self.tear_down()

    def test_paired_end(self):
        FastQC(self.settings).main(
            fq1=f'{self.indir}/trimmed_1.fq',
            fq2=f'{self.indir}/trimmed_2.fq'
        )

    def test_single_end(self):
        FastQC(self.settings).main(
            fq1=f'{self.indir}/trimmed_1.fq',
            fq2=None
        )
