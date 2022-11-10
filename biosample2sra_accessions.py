#!/usr/bin/env python
from xml.etree import ElementTree
import sys
import argparse
import io

from tenacity import retry, wait_exponential
from easy_entrez import EntrezAPI

#@retry(wait=wait_exponential(multiplier=1, min=4, max=10))
def get_sra_accession_from_biosample(biosample_accession: str, entrez_api: EntrezAPI, suppress_warnings: bool) -> str:
    biosample_accession = biosample_accession.strip()
    results = entrez_api.search(biosample_accession, max_results=10, database='sra')
    summary = entrez_api.summarize(results.data['esearchresult']['idlist'][:2], max_results=10, database='sra')
    if ("esummaryresult" in summary.data and summary.data["esummaryresult"][0] == "Empty id list - nothing todo") or "result" not in summary.data:
        if not suppress_warnings:
            print(f"Warning: Couldn't find an SRA entry for BioSample accession {biosample_accession}. Ignoring it.", file=sys.stderr)
        return
    uids = summary.data['result']['uids']
    if len(uids) > 1 and not suppress_warnings:
        print(f"Warning: got multiple ({len(uids)}) uids for the the BioSample accession {biosample_accession}. Will attempt to process all of them.", file=sys.stderr)
    for uid in uids:
        xml_raw = summary.data['result'][uid]['expxml']
        # add a synthetic root which contains the entire xml (doesn't seem to be the case always in the responses)
        xml = '<root>' + xml_raw + '</root>'
        parsed_xml = ElementTree.fromstring(xml)
        sra_accesion = parsed_xml.find("Study").get("acc")
        return sra_accesion

def main(input_file: io.TextIOWrapper, suppress_warnings: bool) -> None:
    entrez_api = EntrezAPI(
        'bio2sra_accessions',
        'matthew@mttmartin.com',
        # optional
        return_type='json'
    )

    for line in input_file:
        sra_accession = get_sra_accession_from_biosample(line, entrez_api, suppress_warnings)
        if sra_accession:
            print(sra_accession)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert BioSample accessions to SRA accessions')
    parser.add_argument("--input-file", type=argparse.FileType('r'), help="Filename of file containing BioSample accessions", default='-')
    parser.add_argument("--suppress-warnings", help="Supress warning messages", action='store_true', dest="suppress_warnings")
    args = parser.parse_args()
    main(args.input_file, args.suppress_warnings)