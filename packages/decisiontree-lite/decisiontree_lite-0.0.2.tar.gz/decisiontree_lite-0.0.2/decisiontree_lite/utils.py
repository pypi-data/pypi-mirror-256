# Import Libraries:

import pandas as pd
import numpy as np
from decisiontree_lite.decisiontree import DecisionTree
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score,confusion_matrix
from sklearn.preprocessing import LabelEncoder
from sklearn.datasets import load_iris, load_wine,load_digits, load_breast_cancer
import time
import warnings
import tracemalloc


# Helper methods to make code setup.

# To load the mentioned dataset.
def load_data(dataset):
    encoder = LabelEncoder()
    if dataset == 'iris':
        iris_data = load_iris(return_X_y=False)
        X, y = iris_data['data'], iris_data['target']
        y = encoder.fit_transform(y)

    if dataset == 'digits':
        digits_data = load_digits(return_X_y=False)
        X, y = digits_data['data'], digits_data['target']
        y = encoder.fit_transform(y)

    elif dataset == 'breast_cancer':
        breast_cancer_data = load_breast_cancer(return_X_y=False)
        X, y = breast_cancer_data['data'], breast_cancer_data['target']
        y = encoder.fit_transform(y)

    elif dataset == 'wine':
        wine_data = load_wine(return_X_y=False)
        X, y = wine_data['data'], wine_data['target']
        y = encoder.fit_transform(y)
    else:
        raise ValueError("Invalid dataset; choose from 'iris', 'digits', 'breast_cancer', 'wine'")
    return X, y

# To validate input datatype
def validate_input(var,txt):
    while True:
        try:
            ab = float(input("Enter {} {}: ".format(var, txt)))
            return ab
        except ValueError:
            print("Warning: Please enter an integer value.")


# To perform test train split based on given test size
def train_test(X, y, tst_split_size):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=tst_split_size ,random_state= 127 )
    return X_train, X_test, y_train, y_test

# Obtain metrics of passed values
def model_metrics(y_test, y_pred):
    warnings.filterwarnings('ignore')
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted')
    recall = recall_score(y_test, y_pred, average='weighted')
    f1score = f1_score(y_test, y_pred, average='weighted')
    return(accuracy, precision, recall, f1score)

# Invokes the custom implementation and returns metrics
def customImplementation(X_train, X_test, y_train, y_test, maxDepth, minSplit, impCriteria):
    # process = psutil.Process(os.getpid())
    # before_cd = process.memory_info().rss
    tracemalloc.start()
    start_time = time.time()
    clf = DecisionTree(max_depth  = maxDepth, min_samples_split = minSplit, criteria = impCriteria)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    end_time = time.time()
    current_memory, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    # after_cd = process.memory_info().rss

    accuracy, precision, recall, f1score = model_metrics(y_test, y_pred)
    time_taken, memory_used = end_time-start_time, (current_memory)/(1024*1024)

    return accuracy, precision, recall, f1score, time_taken, memory_used

# Invokes SKlearns implementation and return metrics.  
def sklearnImplementation(X_train, X_test, y_train, y_test, maxDepth, minSplit, impCriteria):
    # process = psutil.Process(os.getpid())
    # before_code = process.memory_info().rss
    tracemalloc.start()
    start_time = time.time()
    sklearn_clf = DecisionTreeClassifier(max_depth = maxDepth, min_samples_split = minSplit, criterion = impCriteria)   
    sklearn_clf.fit(X_train, y_train)
    skl_prediction = sklearn_clf.predict(X_test)
    end_time = time.time()
    current_memory, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    # after_code = process.memory_info().rss

    accuracy, precision, recall, f1score = model_metrics(y_test, skl_prediction)
    time_taken, memory_used = end_time-start_time, (current_memory)/(1024*1024)
    return accuracy, precision, recall, f1score, time_taken, memory_used