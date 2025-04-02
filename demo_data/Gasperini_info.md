# Enhancer dataset: Gasperini data

## Basic Information

**Technology**: CRISPRi-FlowFISH

**Reference genome**: hg38

**Cell type**: K562 cells

**Publication**: Gasperini et al. (2019) A genome-wide framework for mapping gene regulation via cellular genetic screens

## Sample Size Distribution

- Total number of enhancer-gene pairs: 5,320
- Positive samples (true enhancer-gene pairs): 361
- Negative samples (non-enhancer-gene pairs): 4,957
- Positive sample ratio: 6.8%

## Column Description

The processed data contains the following columns:

1. `chr`: Chromosome name of the enhancer region
2. `start`: Start position of the enhancer region
3. `end`: End position of the enhancer region
4. `gene_name`: Name of the target gene
5. `gene_tss`: Transcription start site (TSS) position of the gene
6. `strand`: DNA strand (+ or -) where the gene is located
7. `distance`: Distance between the enhancer center and gene TSS (in base pairs)
8. `score`: Effect size of the enhancer-gene interaction
9. `label`: Binary label indicating whether the enhancer-gene pair is a true interaction (1) or not (0)



