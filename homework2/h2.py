# -* - coding: UTF-8 -* -
#! /usr/bin/python

"""文本分类
@author:    段雨非<mailto:duanyufeichn@foxmail.com>
@date:      2016-4-7
@stu_num:   3115370071
@desc:      自然语言处理第二次作业
@version:   Python 3.4.3
@reference: https://github.com/itdxer/naive-bayes/
"""

import os
import functools
import chardet
import numpy as np

from skll.metrics import kappa
from nltk.corpus import stopwords
from sklearn.metrics import classification_report,accuracy_score
from sklearn.cross_validation import train_test_split
from naivebayes import NaiveBayesTextClassifier


data_dir = 'data/'

def prepare_file(folder, filename):
    filepath = os.path.join(folder, filename)
    data = open(filepath, 'rb').read()
    codec = chardet.detect(data)
    codec = codec.get('encoding')
    if not codec:
        codec = 'utf-8' 
    return data.decode(codec)

def get_texts(categories):
    documents = []
    classes = []

    for i,category in enumerate(categories):
        category_files_path = os.path.join(data_dir, category)
        text_ids = os.listdir(category_files_path)
        prepare_category_file = functools.partial(prepare_file, category_files_path)
        texts = [prepare_category_file(x) for x in text_ids]
        documents += texts
        classes += [category] * len(texts)

    return documents, classes

def category_to_number(classes, category_type):
    return list(map(category_type.index, classes))

print('> Read files...')
categories = os.listdir(data_dir)
print('> Split data to test and train')
documents, classes = get_texts(categories)
train_docs, test_docs, train_classes, test_classes = train_test_split(
    documents, classes, train_size=0.7)

classifier = NaiveBayesTextClassifier(
    categories=categories,
    min_df=1,
    lowercase=True,
    stop_words=stopwords.words('english')
)

print('> Train classifier')
classifier.train(train_docs, train_classes)

print('> Classify test data...')
predicted_classes = classifier.classify(test_docs)

print('> Complete.')
print(classification_report(test_classes, predicted_classes))

print('-' * 42)
print("{:<25}: {:>4} articles".format("Test data size", len(test_classes)))
print("{:<25}: {:>6.2f} %".format(
    "Accuracy", 100 * accuracy_score(test_classes, predicted_classes))
)
print("{:<25}: {:>6.2f} %".format(
    "Kappa statistics", 100 * kappa(
        category_to_number(test_classes, categories),
        category_to_number(predicted_classes, categories)
    )
))
print('-' * 42)
