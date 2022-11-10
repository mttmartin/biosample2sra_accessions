#!/usr/bin/env python
from xml.etree import ElementTree
import argparse
import io

from tenacity import retry, wait_exponential
from easy_entrez import EntrezAPI


@retry(wait=wait_exponential(multiplier=1, min=4, max=10))
def get_sra_accession_from_biosample(biosample_accession: str, entrez_api: EntrezAPI) -> str:
    results = entrez_api.search(biosample_accession, max_results=10, database='sra')
    summary = entrez_api.summarize(results.data['esearchresult']['idlist'][:2], max_results=10, database='sra')
    uids = summary.data['result']['uids']
    if len(uids) > 1:
        print(f"Warning got multiple ({len(uids)}) uids for the the BioSample accession {biosample_accession}")
    for uid in uids:
        xml_raw = summary.data['result'][uid]['expxml']
        # add a synthetic root which contains the entire xml (doesn't seem to be the case always in the responses)
        xml = '<root>' + xml_raw + '</root>'
        parsed_xml = ElementTree.fromstring(xml)
        sra_accesion = parsed_xml.find("Study").get("acc")
        return sra_accesion

def main(input_file: io.TextIOWrapper) -> None:
    entrez_api = EntrezAPI(
        'bio2sra_accessions',
        'matthew@mttmartin.com',
        # optional
        return_type='json'
    )

    for line in input_file:
        print(get_sra_accession_from_biosample(line, entrez_api))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert BioSample accessions to SRA accessions')
    parser.add_argument("--input-file", type=argparse.FileType('r'), help="Filename of file containing BioSample accessions", default='-')
    args = parser.parse_args()
    main(args.input_file)