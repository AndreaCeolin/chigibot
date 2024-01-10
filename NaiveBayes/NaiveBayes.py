import os
import re
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report

data_folder = '../data'

def extract_sentences(text):
    sentences = re.split(r'\.', text)
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
    return sentences

sentences, labels = [], []

for class_folder in os.listdir(data_folder):
    class_path = os.path.join(data_folder, class_folder)
    if not os.path.isdir(class_path) or class_folder.startswith('.'):
        continue
    for doc_file in os.listdir(class_path):
        doc_path = os.path.join(class_path, doc_file)
        with open(doc_path, 'r', encoding='utf-8') as f:
            text = f.read()
            doc_sentences = extract_sentences(text)
            sentences.extend(doc_sentences)
            labels.extend([class_folder] * len(doc_sentences))

print('Number of Sentences:', len(sentences))

X_train, X_test, y_train, y_test = train_test_split(sentences, labels, test_size=0.2, stratify=labels, random_state=1946)

classifier = Pipeline([
    ('tfidf', TfidfVectorizer(ngram_range=(1, 2), max_features=100000)),
    ('nb', MultinomialNB(alpha=0.01))
])

classifier.fit(X_train, y_train)

y_pred = classifier.predict(X_test)

print('\nClassification Report:')
print(classification_report(y_test, y_pred))