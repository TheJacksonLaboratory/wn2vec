list = ['evaluation', 'dye', 'exclusion', 'colony', 'inhibition', 'technique', 'detection', 'polyoma', 'specific', 'cell', 'mediate', 'immunity', 'cellular', 'immunity', 'direct', 'polyoma', 'virus', 'induced', 'antigen', 'observe', 'c3h', 'hej', 'splenic', 'lymphoid', 'cell', 'ncbitaxon10090', 'sensitize', 'short', 'term', 'immunization', 'schedule', 'syngeneic', 'polyoma', '4198', '4198v', 'meshd009369', 'cell', 'polyoma', 'specificity', 'response', 'show', 'demonstration', 'splenic', 'cell', 'dba', '2j', 'animal', 'meshd014412', 'cytotoxic', 'c3h', '4198', '4198v', 'cell', 'cell', 'another', 'cell', 'line', 'c3h', 'origin', 'polyoma', 'specific', 'response', 'syngeneic', 'system', 'detectable', 'dye', 'exclusion', 'assay', 'colony', 'inhibition', 'procedure', 'colony', 'inhibition', 'cell', 'observe', 'sensitize', 'lymphoid', 'cell', 'allogeneic', 'syngeneic', 'system']

r1 = Replace(list)
r1.arrangement()


class Replace:
    def __init__(self, word):
        self.word = word

        """
    synonym(): Takes a word and prints its synonyms in form of a list (synset) using wordnet 
            @argument: 'word' a string or any variable part of the dataset  
            @return: 'synonyms' a list of synonyms of the words 
    """
    def synonym(word):
        synonyms = []
        for syn in wn.synsets(word):
            for l in syn.lemmas():
                synonyms.append(l.name())
        return synonyms

#list = ['evaluation', 'dye', 'exclusion', 'colony', 'inhibition', 'technique', 'detection', 'polyoma', 'specific', 'cell', 'mediate', 'immunity', 'cellular', 'immunity', 'direct', 'polyoma', 'virus', 'induced', 'antigen', 'observe', 'c3h', 'hej', 'splenic', 'lymphoid', 'cell', 'ncbitaxon10090', 'sensitize', 'short', 'term', 'immunization', 'schedule', 'syngeneic', 'polyoma', '4198', '4198v', 'meshd009369', 'cell', 'polyoma', 'specificity', 'response', 'show', 'demonstration', 'splenic', 'cell', 'dba', '2j', 'animal', 'meshd014412', 'cytotoxic', 'c3h', '4198', '4198v', 'cell', 'cell', 'another', 'cell', 'line', 'c3h', 'origin', 'polyoma', 'specific', 'response', 'syngeneic', 'system', 'detectable', 'dye', 'exclusion', 'assay', 'colony', 'inhibition', 'procedure', 'colony', 'inhibition', 'cell', 'observe', 'sensitize', 'lymphoid', 'cell', 'allogeneic', 'syngeneic', 'system']
testing = ['a', 'cell','b', 'a', 'c', 'b']
#r1 = Replace(amen)
#r1.synonym()
print(testing)
print(testing[1])


synm = []
for syn in wn.synsets('cell'):
    for l in syn.lemmas():
        synm.append(l.name())
print (synm)