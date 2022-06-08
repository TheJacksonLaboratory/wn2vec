output_file = '/Users/niyone/Documents/GitHub/wn2vec/tests/data/output2abstracts.tsv'
marea_file = '/Users/niyone/Documents/GitHub/wn2vec/tests/data/sample2abstracts.tsv'


f = open(marea_file)
y = open(output_file)

content = y.readlines()
count = 0
#print(content[1])
for line in f:
     print(line)
     print(content[count])
     count = count+1

y.close()
f.close()
