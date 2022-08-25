import os, glob
import argparse

def filter_abstract(path_to_pubmed_txt, path_to_pubmed_cr, threshold):
    # Read all txt file in a directory and returns a list of relevant pubmedID
    pubmedId_txt = []
    pubYear_txt = []
    for each_txt in glob.glob(os.path.join(path_to_pubmed_txt, '*.txt')):
        with open(each_txt) as infile:
            for line in infile:
                pubmedID = line.split('##')[0]
                pubYear = int(line.split('##')[1])
                if pubYear > threshold:
                    pubmedId_txt.append(pubmedID)
                    pubYear_txt.append(str(pubYear))
    dict_txt = dict(zip(pubmedId_txt,pubYear_txt))

    # Read all pubmed_cr
    pubmedID_cr = []
    abstracts = []

    with open(path_to_pubmed_cr) as file:
        for line in file:
            pubmedID_cr.append(line.split('\t')[0])
            abstracts.append(line.split('\t')[1])

    dict_cr = dict(zip(pubmedID_cr, abstracts))

    # Map all
    with open('pubmed_filt.tsv', 'a', newline='') as output:
        for pubmedId in pubmedId_txt:
            if pubmedId in dict_cr:
                new_abstract = pubmedId +'\t' + dict_txt.get(pubmedId)+ '\t' + dict_cr.get(pubmedId)
                output.write(new_abstract)


parser = argparse.ArgumentParser()
parser.add_argument('pubmed_txt', type=str) #address of pubmed_txt directory
parser.add_argument('pubmed_cr', type=str) #name of pubmed_cr file
parser.add_argument('threshold', type=int) #name of metadata file
args = parser.parse_args()


filter_abstract(args.pubmed_txt , args.pubmed_cr, args.threshold)

"""

Sample way of running the code:

python newFilter.py 'path_to_pubmed_txt' 'path_to_pubmed_cr' 'threshold' 

ex:  python newFilter.py /Users/niyone/Desktop/wn2vc_marea/test_filter/test_pubmed_txt /Users/niyone/Desktop/wn2vc_marea/test_filter/test_pubmed_cr/100000_test_marea.tsv 2000


"""
