# This script transforms selected mesh sets from MeSH into the format required for WN2VEC.

#from importlib.resources import read_text
import os, glob
import csv
import requests
from csv import DictReader
from collections import defaultdict
import argparse

parser = argparse.ArgumentParser(description='Process MeSH sets   into wn2vec concept set format.')
parser.add_argument('-i', type=str, required=True, help='input directory with MSigDb files')
parser.add_argument('-o', type=str, default='wn2vec_meshsets.tsv',
                    help='name of output file (default=\'wn2vec_meshsets.tsv\'')
args = parser.parse_args()
input_dir = args.i
out_fname = args.o

class MeSHSet:
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


def process_MeSH_file(fname):
    print(f"Processing {fname}")
    if not os.path.isfile(fname):
        raise FileNotFoundError(f"Could not find {fname}")
    mapped_symbols = None
    standard_name = None
    systematicName = None

    mesh_list = []
    with open(fname, 'r') as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            meshid = row[0].split('\t')[0].replace("D","meshd" ) # [0]: 'MAPPED_SYMBOLS', [1]: list of mesh & D000182 --> meshc000657245
            mesh_list.append(meshid)

    standard_name = 'meshset' # This is to hold the position to keep the same format as geneset
    systematicName = 'D0000' # This is to hold the position to keep the same format as geneset
    mapped_symbols = mesh_list

    if mapped_symbols is None or standard_name is None or systematicName is None:
        raise ValueError(f"Could not parse MSigDb gene set properly: {fname}")

    return MeSHSet(name=standard_name, id=systematicName, symbols=mapped_symbols)

mesh_set_list = []

dir_list = os.listdir(input_dir)

for f in dir_list:
    if not f.endswith('.tsv'):
        continue

    fullpath = os.path.join(input_dir, f)
    meshset = process_MeSH_file(fname=fullpath)
    mesh_set_list.append(meshset)

fh = open(out_fname, 'wt')

for meshset in mesh_set_list:
    name = meshset.name
    id = meshset.id
    symbols = meshset.symbols

    fh.write("%s\t%s\t%s\n" % (name, id, ";".join(symbols)))
fh.close()

