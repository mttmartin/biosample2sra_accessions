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

The program expects an input file (or data piped into stdin) containing BioSample accessions. It will print the corresponding SRA accessions to standard out. Each line should contain one accession like:

```
SAMN30650114
SAMN30650017
...
```

An example with an input file on the disk:
```
$ ./biosample2sra_accessions.py --input-file my_biosample_accessions.txt > my_new_sra_accessions.txt
```

Another example using pipes:
```
$ cat my_accessions.txt | ./biosample2sra_accessions.py
```

If a SRA record cannot be found for a given BioSample accession, the default behavior is to print a warning message and continue. If you want to filter or suppress these messages there are two options.

The warnings are printed to standard error and the converted accessions are printed to standard out. So, they can be separated by redirecting them. For example by redirecting the converted accessions to a file:
```
$ cat my_accessions.txt | ./biosample2sra_accessions.py 1> converted_accessions.txt
```

Alternatively, there is a `--suppress-warnings` flag which will suppress all warning messages.
```
cat my_accessions.txt | ./biosample2sra_accessions.py --suppress-warnings
```