from .setup import TestCase
from rna_seq_pipeline.trimming import FastQC, Cutadapt
from os.path import exists


class TestCutadapt(TestCase):

    def setUp(self):
        self.set_up(py_path=__file__)

    def tearDown(self):
        self.tear_down()

    def test_main(self):
        # https://sapac.support.illumina.com/bulletins/2016/12/what-sequences-do-i-use-for-adapter-trimming.html
        # 'AGATCGGAAGAGC' is the 'stem' of the Y-shaped adapter, i.e. the universal adapter sequence
        # read 1 and read 2's adapter sequence should be palindromic, thus fwd and rev should be the same
        fq1, fq2 = Cutadapt(self.settings).main(
            adapter_fwd='AGATCGGAAGAGC',
            adapter_rev='AGATCGGAAGAGC',
            fq1=f'{self.indir}/1month-4NQO-3.1.fq',
            fq2=f'{self.indir}/1month-4NQO-3.2.fq'
        )
        for expected, fq in [
            (f'{self.outdir}/trimmed_1.fq', fq1),
            (f'{self.outdir}/trimmed_2.fq', fq2)
        ]:
            self.assertEqual(expected, fq)
            self.assertTrue(exists(fq))


class TestFastQC(TestCase):

    def setUp(self):
        self.set_up(py_path=__file__)

    def tearDown(self):
        self.tear_down()

    def test_main(self):
        FastQC(self.settings).main(
            trimmed_fq1=f'{self.indir}/trimmed_1.fq',
            trimmed_fq2=f'{self.indir}/trimmed_2.fq'
        )
