"""
=============================================
Feature Union with Heterogeneous Data Sources
=============================================

Datasets can often contain components of that require different feature
extraction and processing pipelines.  This scenario might occur when:

1. Your dataset consists of heterogeneous data types (e.g. raster images and
   text captions)
2. Your dataset is stored in a Pandas DataFrame and different columns
   require different processing pipelines.

This example demonstrates how to use
:class:`sklearn.feature_extraction.FeatureUnion` on a dataset containing
different types of features.  We use the 20-newsgroups dataset and compute
standard bag-of-words features for the subject line and body in separate
pipelines as well as ad hoc features on the body. We combine them (with
weights) using a FeatureUnion and finally train a classifier on the combined
set of features.

The choice of features is not particularly helpful, but serves to illustrate
the technique.
"""

# Author: Matt Terry <matt.terry@gmail.com>
#
# License: BSD 3 clause
from __future__ import print_function

import numpy as np
import csv
import ast
import nltk
import re

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.datasets import fetch_20newsgroups
from sklearn.datasets.twenty_newsgroups import strip_newsgroup_footer
from sklearn.datasets.twenty_newsgroups import strip_newsgroup_quoting
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report
from sklearn.pipeline import FeatureUnion
from sklearn.pipeline import Pipeline
from sklearn.linear_model import SGDClassifier


class ItemSelector(BaseEstimator, TransformerMixin):
    """For data grouped by feature, select subset of data at a provided key.

    The data is expected to be stored in a 2D data structure, where the first
    index is over features and the second is over samples.  i.e.

    >> len(data[key]) == n_samples

    Please note that this is the opposite convention to sklearn feature
    matrixes (where the first index corresponds to sample).

    ItemSelector only requires that the collection implement getitem
    (data[key]).  Examples include: a dict of lists, 2D numpy array, Pandas
    DataFrame, numpy record array, etc.

    >> data = {'a': [1, 5, 2, 5, 2, 8],
               'b': [9, 4, 1, 4, 1, 3]}
    >> ds = ItemSelector(key='a')
    >> data['a'] == ds.transform(data)

    ItemSelector is not designed to handle data grouped by sample.  (e.g. a
    list of dicts).  If your data is structured this way, consider a
    transformer along the lines of `sklearn.feature_extraction.DictVectorizer`.

    Parameters
    ----------
    key : hashable, required
        The key corresponding to the desired value in a mappable.
    """
    def __init__(self, key):
        self.key = key

    def fit(self, x, y=None):
        return self

    def transform(self, data_dict):
        return data_dict[self.key]


class SubjectBodyExtractor(BaseEstimator, TransformerMixin):
    """Extract the subject & body from a usenet post in a single pass.

    Takes a sequence of strings and produces a dict of sequences.  Keys are
    `subject` and `body`.
    """
    def fit(self, x, y=None):
        return self

    def textFeatureExtractor(self, text):
        text = re.sub(r'[^\w\s]',' ',text)
        pos_tok = nltk.word_tokenize(text)
        POS_string=self.POS_converter(text)
        lemma_string=self.stemmer_unigram(text)
        length = ' ' + str(len(pos_tok))
        bigrams = self.word_ngram(text,2)
        result =  length + bigrams + lemma_string

        return result

    def POS_converter(self,text):
        POS_list=nltk.pos_tag(text)
        PoS=[item[1] for item in POS_list]
        string = ' '.join(PoS)
        return string

    def stemmer_unigram(self,token):
        stemmer = nltk.PorterStemmer()
        token=token.split()
        base = [stemmer.stem(t) for t in token]
        string=' '.join(base)
        return string

    def word_ngram(self,token,N):
        if N < 2: return 'please give a number bigger than one'
        else:
            token = token.split(' ')
            output = []
            for m in range(2,N+1):
                for i in range(len(token)-m+1):
                    output.append(token[i:i+m])
            o=[]
            for item in output:
                if len(item)>=2:
                    o.append(''.join(item))
                else:o.append(item[0])
            o=' '.join(o)
            return o    

    def transform(self, posts):
        # posts = ast.literal_eval(posts)
        features = np.recarray(shape=(len(posts),),
                               dtype=[('text', object), ('feature_1', object)])

        for ii in range(len(posts)):
            features['text'][ii] = self.textFeatureExtractor(posts[ii][0])
            features['feature_1'][ii] = posts[ii][1] 
       
        return features


pipeline = Pipeline([
    # Extract the subject & body
    ('subjectbody', SubjectBodyExtractor()),

    # Use FeatureUnion to combine the features from subject and body
    ('union', FeatureUnion(
        transformer_list=[

            # # Pipeline for pulling features from the post's subject line
            ('subject', Pipeline([
                ('selector', ItemSelector(key='feature_1')),
                ('tfidf', TfidfVectorizer(min_df=50)),
            ])),

            # Pipeline for standard bag-of-words model for body
            ('body_bow', Pipeline([
                ('selector', ItemSelector(key='text')),
                ('tfidf', TfidfVectorizer()),
            ])),

            # # Pipeline for pulling ad hoc features from post's body
            # ('body_stats', Pipeline([
            #     ('selector', ItemSelector(key='body')),
            #     ('stats', TextStats()),  # returns a list of dicts
            #     ('vect', DictVectorizer()),  # list of dicts -> feature matrix
            # ])),

        ],

        # weight components in FeatureUnion
        transformer_weights={
            # 'subject': 0.8,
            'body_bow': 1.0,
            # 'body_stats': 1.0,
        },
    )),

    # Use a SVC classifier on the combined features
    ('sgd', SGDClassifier()),
])

train = list(csv.DictReader(open('data/train_multi.csv', 'r')))
test = list(csv.DictReader(open('data/test_multi.csv', 'r')))

# Convert from String to List
train_data = ast.literal_eval(train[0]['data'])
train_target = ast.literal_eval(train[0]['target'])

test_data = ast.literal_eval(test[0]['data'])
test_target = ast.literal_eval(test[0]['target'])

# Debug
# import pdb; pdb.set_trace()

# Run pipeline classifier
pipeline.fit(train_data, train_target)
y = pipeline.predict(test_data)
print(classification_report(y, test_target))
