# bio2sra_accessions

Convert BioSample accessions to SRA accessions. It looks up the accessions using the Entrez API (specifically using `easy_entrez`) and uses an exponential backoff in case of issues retrieving data from the API.

## Installation

You can clone the repository with:
```
$ git clone https://github.com/mttmartin/biosample2sra_accessions.git
```

Dependencies can be installed with pip:
```
$ pip install -r requirements.txt
```

## Usage

The program expects an input file (or data piped into stdin) containing BioSample accessions. Each line should contain one accession like:

```
SAMN30650114
SAMN30650017
...
```

An example with an input file on the disk:
```
$ ./biosample2sra_accessions.py --input-file my_accessions.txt
```

Another example using pipes:
```
$ cat my_accessions.txt | ./biosample2sra_accessions.py
```
