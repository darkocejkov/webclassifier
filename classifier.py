from sklearn.datasets import load_files
from sklearn.naive_bayes import MultinomialNB, CategoricalNB
from featureextraction import tfidf_vector, queries, vectorizer, downscaler
import numpy as np
import pathlib

training_set = load_files("./textset/", encoding="utf-8")

#print(training_set.target_names)  
#y = np.array(queries)

#Cbayes_model = CategoricalNB().fit(tfidf_vector, y)
Mbayes_model = MultinomialNB().fit(tfidf_vector, training_set.target)

#test_docs = ['apex is an amazing battle royale', 'python is a simple language', 'my hobby is playing video games', 'apex is a video game']

test = []
for path in pathlib.Path("./testset/").iterdir():
        if path.is_file():
            current = open(path, "r")
            text = current.read()
            test.append(text)
            current.close()

new_counts = vectorizer.transform(test)
new_tfidf = downscaler.transform(new_counts)

prediction = Mbayes_model.predict(new_tfidf)

for category in prediction:
    print(f"{training_set.target_names[category]}")

print(np.mean(prediction == training_set.target))