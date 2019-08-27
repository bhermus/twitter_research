import json
import numpy as np
from sklearn import datasets
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score

tweets_train = datasets.load_files(container_path='data/')
tweets_test=datasets.load_files(container_path='data/')

text_clf = Pipeline([('vect', CountVectorizer(decode_error='ignore')),
                     ('tfidf', TfidfTransformer()),
                     ('clf', SGDClassifier(loss='hinge', penalty='l2',
                                           alpha=1e-3, random_state=42,
                                           max_iter=5, tol=None)),
])

#count_vect=CountVectorizer(encoding='latin-1')
#tweets_count=count_vect.fit_transform(tweets.data)
print tweets_train.target_names

text_clf.fit(tweets_train.data,tweets_train.target)
scores= cross_val_score(text_clf, tweets_train.data,tweets_train.target, cv=10)
print scores
print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
#predicted=text_clf.predict(tweets_test.data)
#print tweets_test.target
#print predicted
