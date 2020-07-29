from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from os import path, mkdir
import pathlib
import io
import glob
import os
import scipy
from webcrawler import queries #these are the 'targets' of our feature extraction, the classes
# this import allows us to run the webcrawler from this file so we can grab the variables we need

#print(queries)

# the "corpus" of documents is the collection of all documents of relevance for which we want to train on
# first we must make a single text file containing all text within them

corpus_file = '' #a large string containing the corpus
corpus = [] #an array that contains the corpus, with each document in a different index

for query in queries:
    for path in pathlib.Path(f"./textset/{query}/").iterdir():
        if path.is_file():
            current = open(path, "r", encoding="utf-8")
            text = current.read()
            corpus_file += text
            corpus.append(text)
            current.close()

with open("./corpus.txt", "w", encoding="utf-8") as corp:
    corp.write(corpus_file)

#print(corpus[3])
# we will do different techniques of feature extraction, mainly Bag of Words and TFIDF

vectorizer = CountVectorizer()
vector = vectorizer.fit_transform(corpus)
#print(vector.shape)
#indx = vectorizer.vocabulary_.get('shooter') #this vocabulary_ allows us to get the index of a feature
#print(vector[:, indx].toarray()) #we query the matrix to get occurrence of a single feature by [:, index]

downscaler = TfidfTransformer()
tfidf_vector = downscaler.fit_transform(vector) #we fit and transform the previous tokenized and counted feature vector and downscale with TFIDF approach
#print(tfidf_vector.shape)

# scipy.sparse.save_npz('./vector_unscaled.npz', vector) #save feature vectors into .npz (is this necessary?)
# scipy.sparse.save_npz('./vector_tfidf.npz', tfidf_vector) 