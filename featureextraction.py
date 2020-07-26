from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from os import path, mkdir
import pathlib
import io
import glob
import os
from webcrawler import queries #these are the 'targets' of our feature extraction, the classes
# this import allows us to run the webcrawler from this file so we can grab the variables we need

print(queries)

# the "corpus" of documents is the collection of all documents of relevance for which we want to train on
# first we must make a single text file containing all text within them

corpus = ''

for query in queries:
    for path in pathlib.Path(f"./dataset/{query}/text/").iterdir():
        if path.is_file():
            current = open(path, "r", encoding="utf-8")
            text = current.read()
            corpus += text
            current.close()

with open("./corpus.txt", "w", encoding="utf-8") as corp:
    corp.write(corpus)
# we will do different techniques of feature extraction, mainly Bag of Words and TFIDF
