Title: Create a robot with fuzzy decision tree
Date: 2016-02-05
Category: Algorithm
Tag: decision tree, 20 questions


## 0. Related links:
- [A complete fuzzy decision tree technique. Cristina Olaru, Louis Wehenkel](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.85.4051&rep=rep1&type=pdf)

## 1. Background

&nbsp;&nbsp; In order to create a robot to answer 20 questions, I choose fuzzy decision tree to realize it. And I folked a sklearn branch to create new algorithms.


## 2. Learning sklearn.
### 2.1 dataset

```python
>>> from sklearn import datasets
>>> iris = datasets.load_iris()
>>> digits = datasets.load_digits()
```

&nbsp;&nbsp; A dataset is a dictionary-like object that holds all the data and some metadata about the data. This data is stored in the `.data` member, which is `a n_samples`, `n_features` array. In the case of supervised problem, one or more response variables are stored in the `.target` member.


# Reading Tag
- http://scikit-learn.org/stable/tutorial/basic/tutorial.html
- http://scikit-learn.org/stable/datasets/index.html#datasets
