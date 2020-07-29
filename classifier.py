from sklearn.datasets import load_files
from sklearn.naive_bayes import MultinomialNB, CategoricalNB
from featureextraction import tfidf_vector, queries, vectorizer, downscaler
import numpy as np
import pathlib

training_set = load_files("./textset/", encoding="utf-8", shuffle=False)

# for t in training_set.target:
#     print(f"{training_set.target_names[t]} => {training_set.filenames[t]}")

print(training_set.target_names)  
#y = np.array(queries)

#Cbayes_model = CategoricalNB()
#Cbayes_model.fit(tfidf_vector.toarray(), queries)
Mbayes_model = MultinomialNB().fit(tfidf_vector, training_set.target)

#test_docs = ['apex is an amazing battle royale', 'python is a simple language', 'my hobby is playing video games', 'apex is a video game']

test = []
for query in queries:
    for path in pathlib.Path(f"./testset/{query}/").iterdir():
            if path.is_file():
                current = open(path, "r")
                text = current.read()
                test.append(text)
                current.close()

test_set = load_files("./testset/", shuffle=True, encoding="utf-8")

#print(test)

#test = ["I go to university to get a post-secondary education.", "I tested positive for coronavirus, I heard florida has many deaths.", "Tiger king is my favorite show. There are many species of tigers."]

new_counts = vectorizer.transform(test_set.data)
new_tfidf = downscaler.transform(new_counts)

prediction = Mbayes_model.predict(new_tfidf)
#pred = Cbayes_model.predict(new_tfidf)
#print(pred)

# for doc, category in zip(test, prediction):
#     print(f"{doc} => {training_set.target_names[category]}")

print(np.mean(prediction == test_set.target))