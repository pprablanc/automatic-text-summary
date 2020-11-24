#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 14 18:07:02 2018

@author: pierre
"""

import numpy as np
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer

def get_termDocumentMatrix(chapters_processed):

    vectorizer = TfidfVectorizer(ngram_range=(1, 1),
                                    sublinear_tf=True)

    vector_space = list()
    vocabulary = list()
    for c in chapters_processed:
        vector_space.append(np.transpose(vectorizer.fit_transform(c).todense()))
        vocab = vectorizer.get_feature_names()
        vocabulary.append(dict([(s, i) for i, s in enumerate(vocab)]))

    return vocabulary, vector_space