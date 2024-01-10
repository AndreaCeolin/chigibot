import os
import re
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import torch
from simpletransformers.classification import ClassificationModel

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


label_to_int = {'CONTE Giuseppe':0, 'DRAGHI Mario':1, 'GENTILONI SILVERI Paolo':2, 'LETTA Enrico':3, 'MELONI Giorgia':4,  'RENZI Matteo':5}
int_to_label = {value:key for key,value in label_to_int.items()}

print('Number of Training Data:', len(sentences))

X_train, X_test, y_train, y_test = train_test_split(sentences, labels, test_size=0.2, stratify=labels, random_state=1946)

cuda_available = torch.cuda.is_available()

# define hyperparameter
train_args ={"reprocess_input_data": True,
             "overwrite_output_dir": True,
             "fp16":False,
             "num_train_epochs": 5,
             "save_eval_checkpoints" : False,
             "save_model_every_epoch": False,
             "save_optimizer_and_scheduler" : False,
             "save_steps": False}

# Create a ClassificationModel
model = ClassificationModel(
    #"bert", "dbmdz/bert-base-italian-xxl-cased", # when the model is first trained, we must fetch it directly from HuggingFace
    "bert", "fine_tuned_bert-base-italian-xxl-cased_5", # when the model has been trained, we can fetch a local copy
    use_cuda=cuda_available,
    num_labels=6,
    args=train_args
)

import pandas as pd

train_df = pd.DataFrame([[X,label_to_int[y]] for X,y in zip(X_train,y_train)], columns=['text', 'label'])
test_df = pd.DataFrame([[X,label_to_int[y]] for X,y in zip(X_test,y_test)], columns=['text', 'label'])

print(train_df.shape)
print(test_df.shape)

'''
model.train_model(train_df)

model.model.save_pretrained('fine_tuned_bert-base-italian-xxl-cased_5')
model.tokenizer.save_pretrained('fine_tuned_bert-base-italian-xxl-cased_5')
model.config.save_pretrained('fine_tuned_bert-base-italian-xxl-cased_5')
'''

predictions, raw_outputs = model.predict(X_test)

print('\nClassification Report:')
print(classification_report(predictions, test_df['label']))