# Contains the scripts for performing the text mining on the Jim cases
The various files are as follows

## FindNounPhrasesUsingSpacy.ipynb
This script uses the spacy.io library to find out the various noun phrases

## Kmeans_clustering.ipynb
This is responsible to perform teh clustering using the kmeans. The output is the tags and the cases it appears into

## TokenizeCases.ipynb
This is the one that will transform the cases to normalized version of the case by applying the ngram tokenization. This is equivalent to the tokenizecaseDatausingDictionaryInSingleStep.php

## createNGramDictionary.ipynb
This will create the dictionary based on the ngrm counts, pos, spacy
