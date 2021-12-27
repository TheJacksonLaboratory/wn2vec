# wn2vec
Wordnet 2 vector


I have added some skeleton Python code to get us started.

This part of the project serves one purpose -- to substitute texts with one ID per synonym set to reduce the overall number of
vectors that result from Word2vec. Other parts of the project will be developed later on to see if this approach improves
the overall utility of word2vec embedding.

We will create a simple python package to ease testing and use in notebooks or scripts, called ``wn2vec``.


To run this code, we need the NLTK library. To set this up, I recommend the following

```
python3 -m venv mykernel
source mykernel/bin/activate
pip install nltk
```

We can develop the functionality of the code in a notebook by adding the following

```
source mykernel/bin/activate # only needed once per session
pip install jupyter
ipython kernel install --name "mykernel" --user
```

Start with ``jupyter-lab`` or ``jupyter notebook`` and choose ``mykernel``. See the notebook at ``notebook/nltkdemo.ipynb`` for how to use the python package we are creating, ``wn2vec``.
