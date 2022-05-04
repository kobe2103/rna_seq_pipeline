# RNA-seq Pipeline

## Usage

```bash
git clone https://github.com/kobe2103/rna_seq_pipeline
```

Paired-end mode

```bash
python rna_seq_pipeline \
  -r reference_genome.fa \
  -g gene_annotation.gtf \
  -1 read1.fq.gz \
  -2 read2.fq.gz
```

Single-end mode

```bash
python rna_seq_pipeline \
  -r reference_genome.fa \
  -g gene_annotation.gtf \
  -1 read.fq.gz
```

## Environment

Required packages:
- `cutadapt`
- `fastqc`
- `bowtie2`
- `samtools`
- `star`
- `HTseq`

Create a conda environment `rna-seq` and install packages:

```bash
conda create --name rna-seq
conda activate rna-seq
conda install -c bioconda cutadapt fastqc bowtie2 samtools star
pip install HTseq
```
