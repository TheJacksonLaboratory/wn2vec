# Stop words
## How Marea Handles Stop Words

Marea's approach to handling stop words includes several criteria:

- Whether lowercase or Capitalized.
- Marea starts with the NLTK stop word list for English and adds some new stop words.
- Any token that starts with a digit (even if the rest of the string includes some letters) is treated as numerical and discarded if it is not one of the interesting numbers.
- Any letter of the alphabet that occurs as a single-character token is a stop word.

### NLTK Stop Words

The NLTK Stop Words can be found at [NLTK Stop Words](https://pythonspot.com/nltk-stop-words/).

Currently, there are 179 English stop words:


{"doesn't", 'she', "hasn't", 'the', 'yourself', 'ma', 'what', 'aren', 'from', 'me', 'haven', 'which', 'on', 'no', 'your', 'him', 'being', 'they', 'whom', 'weren', 'off', 'herself', 'couldn', 'so', 'should', 'them', 'all', 'any', 'd', 'more', 'we', 'as', 'each', 'hadn', 'theirs', 'needn', 'few', "you've", 'or', 'it', 'our', 'in', 'does', 'very', 'isn', 'mightn', 'was', 'then', 'under', 'before', 'but', 'below', 'further', 'himself', 've', "wasn't", 'only', 'ain', "you'll", 'mustn', 'hers', 'for', 'where', "hadn't", 'his', 'yourselves', "it's", "won't", "you'd", 'are', 'some', 't', 'been', 'such', 'when', 'shan', 'during', "didn't", 'i', 'is', 'were', "mightn't", 'own', "shan't", 'had', 'by', "shouldn't", 'up', 'out', 'ourselves', 'because', 'at', 'who', 'how', 'with', 'to', 'doing', "don't", 'of', 'wouldn', 'too', 'do', 'a', 'once', 'down', 'don', "isn't", 'than', 'this', 'm', 'these', 'through', 're', 'my', 'doesn', "weren't", 'll', 'you', 'if', "you're", 'here', 'her', "mustn't", 'wasn', 'just', "she's", 'have', 'an', 'he', 'myself', 'and', 'didn', 'y', 'themselves', "couldn't", 'o', 'did', 'against', 'can', "aren't", "should've", 'into', 'while', 'its', 'both', 'ours', 'again', 'won', 'after', 'has', 'most', 'until', 's', 'hasn', "that'll", 'those', 'am', 'yours', 'there', 'now', 'over', 'itself', 'nor', 'above', "haven't", 'between', 'other', 'having', 'why', 'their', 'will', "wouldn't", 'about', 'not', "needn't", 'that', 'be', 'shouldn', 'same'}


### Additional Stop Words

Marea includes additional stop words:


'also', 'cannot', 'could', 'furthermore', 'however','may', 'might', 'non', 'thus', 'whose', 'within','without', 'would'



### Interesting Numbers

Marea treats the following numbers as interesting and does not discard them:



interesting_numbers = {'001', '01', '05', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '95', '99', '100'}


