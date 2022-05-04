FROM continuumio/miniconda3:4.10.3

RUN conda create -n rna-seq \
 && conda install -c conda-forge -n rna-seq \
    tbb=2020.2 \
 && conda install -c bioconda -n rna-seq \
    cutadapt=4.0 \
    samtools=1.11 \
    bowtie2=2.3.5 \
    star=2.7.10 \
    fastqc=0.11.9 \
 && conda clean --all --yes

ENV PATH /opt/conda/envs/rna-seq/bin:$PATH

RUN /opt/conda/envs/rna-seq/bin/pip install --no-cache-dir \
    HTSeq==2.0.1

COPY rna_seq_pipeline/* /rna_seq_pipeline/rna_seq_pipeline/
COPY ./__main__.py /rna_seq_pipeline/__main__.py
WORKDIR /
