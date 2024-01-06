# Chigibot

This repository contains a corpus of political speeches from Italian Prime Ministers in the Camera dei Deputati Legislature XVII, XVIII and XIX (2013-2024). 

Six different Prime Ministers were appointed in this period (Enrico Letta, Matteo Renzi, Paolo Gentiloni, Giuseppe Conte, Mario Draghi and Giorgia Meloni), and they cover basically every part of the political spectrum.

The repository contains the following files:

1. **data**: this folder contains six folders named after the Prime Ministers, and a Python script that was used to extract the speeches from [http://documenti.camera.it](http://documenti.camera.it). 

2. **NaiveBayes**: this folder contains a Jupyter Notebook with a simple Naive Bayes classifier.

3. **BERT**: this folder contains a Jupyter Notebook with a BERT model trained using the library `simpletransformers`.

An app that uses the classifier models to predict new political statements has been deployed to [http://chigibot.eu.pythonanywhere.com](http://chigibot.eu.pythonanywhere.com) (only the Naive Bayes classifier is used at the moment).

If you cite/use material from this repo, please cite the repository URL:

Ceolin, A. (2024). Chigibot. https://github.com/AndreaCeolin/chigibot
