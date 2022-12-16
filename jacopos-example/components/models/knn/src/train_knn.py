import kfp
from kfp.v2 import dsl
from kfp.v2.dsl import Dataset, Model, Input, Output, component
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TARGET_IMAGE = 'jackma00/train-knn:latest'

@component(
    base_image='python:3.8',
    target_image=TARGET_IMAGE,
    packages_to_install=['pandas', 'scikit-learn']
)
def train_knn(
    normalized_dataset: Input[Dataset],
    model: Output[Model],
    n_neighbors: int):
    """The function trains and serializes a knn model."""

    with open(normalized_dataset.path) as f:
        df = pd.read_csv(f)

    y = df.pop('Labels')
    X = df

    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

    clf = KNeighborsClassifier(n_neighbors=n_neighbors)
    clf.fit(X_train, y_train)
    with open(model.path, 'wb') as f:
        pickle.dump(clf, f)