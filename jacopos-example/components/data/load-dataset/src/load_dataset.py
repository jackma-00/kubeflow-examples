import kfp
from kfp.v2 import dsl
from kfp.v2.dsl import Dataset, Output, component
import pandas as pd

TARGET_IMAGE = 'jackma00/load-dataset:latest'

@component(
    base_image='python:3.8',
    target_image=TARGET_IMAGE,
    packages_to_install=['pandas']
)
def load_dataset(dataset: Output[Dataset]):
    """The function load and save the dataset from the given URL."""

    # URL where to retrieve the dataset
    csv_url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data'
    
    # using the attribute information as the column names
    col_names = [
        'Sepal_Length', 'Sepal_Width', 'Petal_Length', 'Petal_Width', 'Labels'
    ]

    # Load dataset
    df = pd.read_csv(csv_url, names=col_names)

    # Save dataset
    with open(dataset.path, 'w') as f:
        df.to_csv(f)