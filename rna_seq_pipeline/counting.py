import io
import pandas as pd
from typing import Dict
from .template import Processor


class Counting(Processor):

    FEATURE_TYPES = [
        'gene', 'exon', 'UTR'
    ]

    sorted_bam: str
    gtf: str

    feature_type_to_count_txt: Dict[str, str]
    count_csv: str
    other_count_txt: str

    def main(self,
             sorted_bam: str,
             gtf: str) -> str:

        self.sorted_bam = sorted_bam
        self.gtf = gtf

        self.index_bam()
        self.count_feature_types()
        self.write_count_tsv()
        self.write_other_count_txt()

        return self.count_csv

    def index_bam(self):
        self.call(f'samtools index {self.sorted_bam}')

    def count_feature_types(self):
        self.feature_type_to_count_txt = {}
        for feature_type in self.FEATURE_TYPES:
            count_txt = self.__htseq_count(feature_type)
            self.feature_type_to_count_txt[feature_type] = count_txt

    def __htseq_count(self, feature_type: str) -> str:
        return HTSeqCount(self.settings).main(
            sorted_bam=self.sorted_bam,
            gtf=self.gtf,
            feature_type=feature_type)

    def write_count_tsv(self):
        self.count_csv = WriteCountCsv(self.settings).main(
            feature_type_to_count_txt=self.feature_type_to_count_txt)

    def write_other_count_txt(self):
        self.other_count_txt = WriteOtherCountTxt(self.settings).main(
            feature_type_to_count_txt=self.feature_type_to_count_txt)


class HTSeqCount(Processor):

    STANDARD_SPECIFIC_ASSAY = 'yes'
    SKIP_LOWER_QUALITY_READ = '10'
    MODE_TO_HANDLE_READ_OVERLAPPING = 'union'
    ID_ATTRIBUTE = 'gene_id'

    sorted_bam: str
    gtf: str
    feature_type: str

    output_txt: str

    def main(self,
             sorted_bam: str,
             gtf: str,
             feature_type: str) -> str:

        self.sorted_bam = sorted_bam
        self.gtf = gtf
        self.feature_type = feature_type

        self.execute()

        return self.output_txt

    def execute(self):
        self.output_txt = f'{self.workdir}/htseq-count-{self.feature_type}.txt'
        log = f'{self.outdir}/htseq-count-{self.feature_type}.log'
        cmd = f'''htseq-count \\
--format bam \\
--order name \\
--stranded {self.STANDARD_SPECIFIC_ASSAY} \\
-a {self.SKIP_LOWER_QUALITY_READ} \\
--type {self.feature_type} \\
--idattr {self.ID_ATTRIBUTE} \\
--mode {self.MODE_TO_HANDLE_READ_OVERLAPPING} \\
--nonunique all \\
{self.sorted_bam} \\
{self.gtf} \\
1> {self.output_txt} \\
2> {log}'''
        self.call(cmd)


class WriteCountCsv(Processor):

    ID_COLUMN = 'gene_id'

    feature_type_to_count_txt: Dict[str, str]

    df: pd.DataFrame
    output_csv: str

    def main(self, feature_type_to_count_txt: Dict[str, str]) -> str:
        self.feature_type_to_count_txt = feature_type_to_count_txt

        self.init_df()
        for feature_type, count_txt in self.feature_type_to_count_txt.items():
            df = self.read_count_txt(feature_type, count_txt)
            self.merge(df)
        self.write_csv()

        return self.output_csv

    def init_df(self):
        self.df = pd.DataFrame(columns=[self.ID_COLUMN])

    def read_count_txt(
            self,
            feature_type: str,
            count_txt: str) -> pd.DataFrame:

        lines = []
        with open(count_txt) as fh:
            for line in fh:
                if not line.startswith('__'):
                    lines.append(line.strip())

        return pd.read_csv(
            io.StringIO('\n'.join(lines)),
            sep='\t',
            names=[self.ID_COLUMN, feature_type]
        )

    def merge(self, df: pd.DataFrame):
        self.df = self.df.merge(
            right=df,
            on=self.ID_COLUMN,
            how='outer')

    def write_csv(self):
        self.output_csv = f'{self.outdir}/counts.csv'
        self.df.to_csv(self.output_csv, index=False)


class WriteOtherCountTxt(Processor):

    feature_type_to_count_txt: Dict[str, str]

    content: str
    output_txt: str

    def main(self, feature_type_to_count_txt: Dict[str, str]) -> str:
        self.feature_type_to_count_txt = feature_type_to_count_txt

        self.content = ''
        for feature_type, count_txt in self.feature_type_to_count_txt.items():
            self.content += self.read_count_txt(feature_type, count_txt)
        self.write_output_txt()

        return self.output_txt

    def read_count_txt(
            self,
            feature_type: str,
            count_txt: str) -> str:

        lines = [f'# count by {feature_type}']

        with open(count_txt) as fh:
            for line in fh:
                if line.startswith('__'):
                    lines.append(line.strip())

        return '\n'.join(lines) + '\n\n'

    def write_output_txt(self):
        self.output_txt = f'{self.outdir}/other-counts.txt'
        with open(self.output_txt, 'w') as fh:
            fh.write(self.content.rstrip() + '\n')
