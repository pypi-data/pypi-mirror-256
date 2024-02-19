# Importing Libraries:

import pandas as pd
import numpy as np



# Class to create a node in the decision tree.
class Node:
    def __init__(self, feature=None, threshold=None, left=None, right=None, value=None):
        self.feature = feature
        self.threshold = threshold
        self.left = left
        self.right = right
        self.value = value
    
    # To check if a node is a leaf node or not
    def is_leaf(self):
        return self.value is not None

# Class to create and train a decision tree.
class DecisionTree:
    def __init__(self, max_depth=100, min_samples_split=2, criteria = 'entropy'):
        if max_depth <= 0:
            raise ValueError('max_depth should be >= 1')
        if min_samples_split <= 1:
            raise ValueError('min_samples_split should be >= 2')
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.root = None
        self.criteria = criteria

    # To calculate the impurity of a given dataset using Gini or entropy
    def impurity_measure(self, y, criteria):
        proportions = np.bincount(y) / len(y)
        lt = []
        impurity_val = None
        if criteria == 'gini':
            impurity_val = 1 - np.sum([p**2 for p in proportions])
        else:
            impurity_val = -np.sum([p * np.log2(p) for p in proportions if p > 0])
        return impurity_val

    # To check if the algorithm should stop building the tree
    def _stop_check(self, depth):
        if (depth >= self.max_depth or self.num_target_labels == 1 or self.num_observations < self.min_samples_split):
            return True
        return False

    # To find the best feature and threshold value to split the data
    def _best_split(self, X, y, features):
        gain = - 1
        feature =  None
        threshold = None
        for f in features:
            X_feature = X[:, f]
            thresholds = np.unique(X_feature)
            for t in thresholds:
                ig = self._information_gain(X_feature, y, t)
                if ig > gain:
                    gain = ig
                    feature = f
                    threshold = t
        return feature, threshold

    # To split the data based on a given threshold
    def _splitter(self, X, threshold):
        left_indx = np.argwhere(X <= threshold).flatten()
        right_indx = np.argwhere(X > threshold).flatten()
        return left_indx, right_indx

    # To calculate the information gain for a given split data.
    def _information_gain(self, X, y, threshold):
        if self.criteria == 'gini':
            parent_impurity = self.impurity_measure(y,'gini')
        else:
            parent_impurity = self.impurity_measure(y,'entropy')

        left_indx, right_indx = self._splitter(X, threshold)
        n, n_left, n_right = len(y), len(left_indx), len(right_indx)
        if n_left == 0 or n_right == 0: 
            return 0

        if self.criteria == 'gini':
            impurity_left = self.impurity_measure(y[left_indx],'gini')
            impurity_right = self.impurity_measure(y[right_indx],'gini')
        else:
            impurity_left = self.impurity_measure(y[left_indx],'entropy')
            impurity_right = self.impurity_measure(y[right_indx],'entropy')

        child_impurity = (n_left / n) * impurity_left + (n_right / n) * impurity_right
        return parent_impurity - child_impurity

    # To recursively build the decision tree
    def build_tree(self, X, y, depth=0):
        self.num_observations, self.num_features = X.shape
        self.num_target_labels = len(np.unique(y))

        # To stop the tree based on given criteria
        if self._stop_check(depth):
            most_common_element = np.argmax(np.bincount(y))
            return Node(value = most_common_element)

        random_features = np.random.choice(self.num_features, self.num_features, replace=False)

        best_feature, best_threshold = self._best_split(X, y, random_features)

        left_indx, right_indx = self._splitter(X[:, best_feature], best_threshold)
        left_child = self.build_tree(X[left_indx, :], y[left_indx], depth + 1)
        right_child = self.build_tree(X[right_indx, :], y[right_indx], depth + 1)
        return Node(best_feature, best_threshold, left_child, right_child)
    
    def _traverse_tree(self, x, node):
        if node.is_leaf():
            return node.value

        if x[node.feature] <= node.threshold:
            return self._traverse_tree(x, node.left)
        return self._traverse_tree(x, node.right)

    def fit(self, X, y):
        self.root = self.build_tree(X, y)

    def predict(self, X):
        predictions = [self._traverse_tree(x, self.root) for x in X]
        return np.array(predictions)