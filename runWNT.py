from scripts import WordNetTransformer


marea_file = "data/sample100abstracts.tsv"

transformer = WordNetTransformer(marea_file)

with open(marea_file) as f:
    for line in f:
        fields = line.split('\t')
        abstract_text = fields[2]
        transformed_text = transformer.transform(abstract_text)
        print(abstract_text)
        print(transformed_text)
        print()

