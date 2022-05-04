import os
import shutil
import unittest
from rna_seq_pipeline.template import Settings


class TestCase(unittest.TestCase):

    def set_up(self, py_path: str):
        self.indir = py_path[:-3]
        basedir = os.path.dirname(__file__)
        self.workdir = f'{basedir}/workdir'
        self.outdir = f'{basedir}/outdir'

        for d in [self.workdir, self.outdir]:
            os.makedirs(d, exist_ok=True)

        self.settings = Settings(
            workdir=self.workdir,
            outdir=self.outdir,
            threads=6,
            debug=True)

    def tear_down(self):
        for d in [self.workdir, self.outdir]:
            shutil.rmtree(d)

    def assertFileExists(self, expected: str, actual: str):
        self.assertEqual(expected, actual)
        self.assertTrue(os.path.exists(actual))
