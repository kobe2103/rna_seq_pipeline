from .setup import TestCase
from rna_seq_pipeline.counting import Counting, HTSeqCount, WriteCountCsv, WriteOtherCountTxt


class TestCounting(TestCase):

    def setUp(self):
        self.set_up(py_path=__file__)

    def tearDown(self):
        self.tear_down()

    def test_main(self):
        actual = Counting(self.settings).main(
            sorted_bam=f'{self.indir}/sorted.bam',
            gtf=f'{self.indir}/21_0501_subset_mouse_genome.gtf',
            min_count_mapq=10,
            nonunique_count='all',
            stranded_count='yes',
        )
        expected = f'{self.indir}/counts.csv'
        self.assertFileEqual(expected, actual)


class TestHTSeqCount(TestCase):

    def setUp(self):
        self.set_up(py_path=__file__)

    def tearDown(self):
        self.tear_down()

    def test_main(self):
        actual = HTSeqCount(self.settings).main(
            sorted_bam=f'{self.indir}/sorted.bam',
            gtf=f'{self.indir}/21_0501_subset_mouse_genome.gtf',
            min_count_mapq=10,
            nonunique_count='none',
            stranded_count='yes',
            feature_type='exon'
        )
        expected = f'{self.workdir}/htseq-count-exon.txt'
        self.assertFileExists(expected, actual)


class TestWriteCountCsv(TestCase):

    def setUp(self):
        self.set_up(py_path=__file__)

    def tearDown(self):
        self.tear_down()

    def test_main(self):
        WriteCountCsv(self.settings).main(
            feature_type_to_count_txt={
                'gene': f'{self.indir}/htseq/htseq-count-gene.txt',
                'exon': f'{self.indir}/htseq/htseq-count-exon.txt',
                'UTR': f'{self.indir}/htseq/htseq-count-UTR.txt'
            }
        )


class TestWriteOtherCountTxt(TestCase):

    def setUp(self):
        self.set_up(py_path=__file__)

    def tearDown(self):
        self.tear_down()

    def test_main(self):
        WriteOtherCountTxt(self.settings).main(
            feature_type_to_count_txt={
                'gene': f'{self.indir}/htseq/htseq-count-gene.txt',
                'exon': f'{self.indir}/htseq/htseq-count-exon.txt',
                'UTR': f'{self.indir}/htseq/htseq-count-UTR.txt'
            }
        )
