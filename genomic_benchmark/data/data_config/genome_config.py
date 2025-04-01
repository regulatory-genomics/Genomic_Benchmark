"""
Reference genome configuration
"""

GENOME_CONFIG = {
    "hg19": {
        "fasta_url": "https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_19/GRCh37.p13.genome.fa.gz",
        "gtf_url": "https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_19/gencode.v19.annotation.gtf.gz"
    },
    "hg38": {
        "fasta_url": "https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_47/GRCh38.p14.genome.fa.gz",
        "gtf_url": "https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_47/gencode.v47.annotation.gtf.gz"
    },
    "mm10": {
        "fasta_url": "https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_mouse/release_M36/GRCm39.genome.fa.gz",
        "gtf_url": "https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_mouse/release_M36/gencode.vM36.annotation.gtf.gz"
    }
} 