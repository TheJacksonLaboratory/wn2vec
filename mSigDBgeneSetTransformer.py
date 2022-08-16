# This script transforms selected gene sets from MSigDb into the format required for WN2VEC.
# Note that we have performed the transformation and stored the genesets in the data/conceptsets directory
# and this script is not required to use WN2VEC

#from importlib.resources import read_text
import os
import requests
from csv import DictReader
from collections import defaultdict
import argparse

parser = argparse.ArgumentParser(description='Process MSigDb genesets into wn2vec concept set format.')
parser.add_argument('-i',  type=str, required=True, help='input directory with MSigDb files')
parser.add_argument('-o', type=str, default='wn2vec_genesets.tsv',
                    help='name of output file (default=\'wn2vec_genesets.tsv\'')
args = parser.parse_args()
input_dir = args.i
out_fname = args.o



hgncUrl = "http://ftp.ebi.ac.uk/pub/databases/genenames/hgnc/tsv/non_alt_loci_set.txt"
hgncFilename = "non_alt_loci_set.txt"

# download file if needed
if not os.path.isfile(hgncFilename):
    response = requests.get(hgncUrl)
    open(hgncFilename, "wb").write(response.content)

symbol_to_entrez_id_dict = defaultdict(str)

with open(hgncFilename) as f:
    r = DictReader(f, delimiter='\t')
    for row in r:
        symbol_to_entrez_id_dict[row['symbol']] = row['entrez_id']



class MSigDbGeneSet:
    def __init__(self, name, id, symbols):
        self._name = name
        self._id = id
        self._symbols = symbols

    @property
    def name(self):
        return self._name

    @property
    def id(self):
        return self._id

    @property
    def symbols(self):
        return self._symbols


def process_MSigDb_file(fname):
    print(f"Processing {fname}")
    if not os.path.isfile(fname):
        raise FileNotFoundError(f"Could not find {fname}")
    mapped_symbols = None
    standard_name = None
    systematicName = None
    with open(fname) as f:
        for line in f:
            fields = line.rstrip().split('\t')
            if len(fields) == 2:
                fieldname = fields[0]
                if fieldname == 'MAPPED_SYMBOLS':
                    mapped_symbols = fields[1]
                elif fieldname == 'STANDARD_NAME':
                    standard_name  = fields[1]
                elif fieldname == 'SYSTEMATIC_NAME':
                    systematicName = fields[1]
    # when we get here, we should have all three bits of information
    if mapped_symbols is None or standard_name is None or systematicName is None:
        raise ValueError(f"Could not parse MSigDb gene set properly: {fname}")
    mapped_symbols_list = mapped_symbols.split(",")
    return MSigDbGeneSet(name=standard_name, id=systematicName, symbols=mapped_symbols_list)
    




gene_set_list = []

dir_list = os.listdir(input_dir)
for f in dir_list:
    fullpath = os.path.join(input_dir, f)
    geneset = process_MSigDb_file(fname=fullpath)
    gene_set_list.append(geneset)


fh = open(out_fname, 'wt')
for geneset in gene_set_list:
    name = geneset.name
    id = geneset.id
    symbols = geneset.symbols
    replaced_symbols = [f"ncbigene{symbol_to_entrez_id_dict.get(symbol)}" for symbol in symbols if symbol in symbol_to_entrez_id_dict]
    fh.write("%s\t%s\t%s\n" % (name, id, ";".join(replaced_symbols)))
fh.close()
    
