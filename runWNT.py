
from script import Replace

marea_file = "data/sample100abstracts.tsv"

#transformer = WordNetTransformer(marea_file)

replace = Replace(marea_file)
replaced_data = replace.get_replaced_data()
print(replaced_data)