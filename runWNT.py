from csv import DictReader
from wn2vec import WordNetTransformer

marea_file = "data/sample100abstracts.tsv"

transformer = WordNetTransformer(marea_file)

with open(marea_file) as f:
    reader = DictReader(f, delimiter="\t")
    for row in reader:
        print(row)