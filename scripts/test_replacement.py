
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-i', type=str, help ='address of wordnet transformer output') #address of the filtred marea file
parser.add_argument('-r', type=str, help ='address of replaceed_words output') #address of output file
args = parser.parse_args()

pubmed_wn = args.i
replaced = args.r


#Read Replaced words
data = []
with open(replaced,"r") as v:
    data = v.readlines() 

replaced = data[3]



#Read Transformed Text
pubmed_wn_tokens = []
non_replaced = []
with open(pubmed_wn) as f:
  for line in f:
        columns = line.split('\t')
        if len(columns) != 3:
            raise ValueError(f'Malformed marea line: {line}')

        payload = columns[2] # columns[0] - year, columns[1]: pmid, columns[2] abstract text
        words = payload.split()
        for word in words:
          if word in replaced:
            non_replaced = []
        pubmed_wn_tokens.extend(words)


# Test

if len(non_replaced) == 0:
  print("All words replaced")

else:
  print("words not replace:")
  print(non_replaced)