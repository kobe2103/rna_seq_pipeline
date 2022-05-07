from typing import Tuple
from os.path import basename
from .template import Processor


class CopyRefFiles(Processor):

    ref_fa: str
    gtf: str

    copied_ref_fa: str
    copied_gtf: str

    def main(self, ref_fa: str, gtf: str) -> Tuple[str, str]:
        self.ref_fa = ref_fa
        self.gtf = gtf

        self.unzip_or_copy_ref_fa()
        self.unzip_or_copy_gtf()

        return self.copied_ref_fa, self.copied_gtf

    def unzip_or_copy_ref_fa(self):
        self.copied_ref_fa = self.__get_copied_path(self.ref_fa)
        self.__unzip_or_copy(self.ref_fa, self.copied_ref_fa)

    def unzip_or_copy_gtf(self):
        self.copied_gtf = self.__get_copied_path(self.gtf)
        self.__unzip_or_copy(self.gtf, self.copied_gtf)

    def __get_copied_path(self, src: str) -> str:
        fname = basename(src)
        if src.endswith('.gz'):
            fname = fname[:-3]
        return f'{self.workdir}/{fname}'

    def __unzip_or_copy(self, src, dst):
        if src.endswith('.gz'):
            cmd = f'gzip --decompress --stdout {src} > {dst}'
        else:
            cmd = f'cp {src} {dst}'
        self.call(cmd)
