#! /usr/bin/env python3.5

# NOTE: Code to lemmatise the extracted text within scrapy itself. Test run
# with scrapy to see if they work

# Importing modules
import string
import re
import sys
import treetaggerwrapper
from nltk.tokenize import word_tokenize

## Clean the provided text with lemmatisation and NO stopword removal

def clean_text(articles):
    # Cleans the relevant text and returns a string
    # with numbers and punctation, and with lower text.
    # Depends on a system parameter @FileName

    # Function defaults
    # Read in the text
    text = articles

    # Removing URL links from text
    text = re.sub(r'http\S+', "", text)

    # Tokenising text
    text = re.split('[?.,:;!\s]', text)

    text = [word for word in text if word]

    # Converting tokensied words back to string
    text = " ".join(word for word in text)

    # Returning text
    return text

def lemmatise_dict(text):
    # Lemmatises the available text and returns a
    # Dictionary with tokens and their lemma. will
    # return a dictionary with the lemmatised word
    # Requires a list of strings and the parameter @lang

    # Defining the tag language
    tag_lang = 'de'

    # Tokenising text and creating a list of unique words
    text = re.split('[?.,:;!\s]', text)

    unique_words = []
    for words in text:
        if words not in unique_words:
            unique_words.append(words)

    text = " ".join(word for word in unique_words)

    # Defining tagger
    tagger = treetaggerwrapper.TreeTagger(TAGLANG=tag_lang)

    # Tagging words
    tags = tagger.tag_text(text)

    text = [i.split("\t") for i in tags]

    # Generating Dictionary
    text_dict = {}
    for x in text:
        token = x[0]
        if x[2] == "@card@":
            lemma = x[0]
        else:
            lemma = x[2]
        text_dict[token] = lemma

    return text_dict


def replace_words(text, dict):
    # Pattern of whole words only
    for token, lemma in dict.items():
        text = text.replace(token, lemma)
    return text


def lemmatise_text(articles):
    # Function to read, clean and lemmatise text
    cleaned_text = clean_text(articles)
    lemma_dict = lemmatise_dict(cleaned_text)

    # Looping over the lists of text
    lemma_text = replace_words(cleaned_text, lemma_dict)

    return lemma_text
