# load_dataset_component.py
import pandas as pd
from kfp.v2.dsl import (
  component,
  Dataset,
  Output,
) 

@component(
    base_image='python:3.8',
    target_image='jackma00/load-dataset:latest',
    packages_to_install=['pandas'],
)
def load_dataset(
    dataset: Output[Dataset]
):
    """The function load and save the dataset from the given URL."""

    # URL where to retrieve the dataset
    csv_url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data'
    
    # using the attribute information as the column names
    col_names = ['Sepal_Length','Sepal_Width','Petal_Length','Petal_Width','Class']
    
    # Load the dataset 
    iris =  pd.read_csv(csv_url, names = col_names)

    # Save the dataset
    with open(dataset.path, 'w') as f:
        iris.to_csv(f)