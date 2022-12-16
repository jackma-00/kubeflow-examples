import kfp
from kfp.v2 import dsl
from kfp.v2.dsl import Dataset, Input, Output, component
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler

TARGET_IMAGE = 'jackma00/normalize-dataset:latest'

@component(
    base_image='python:3.8',
    target_image=TARGET_IMAGE,
    packages_to_install=['pandas', 'scikit-learn']
)
def normalize_dataset(
    input_dataset: Input[Dataset],
    normalized_dataset: Output[Dataset],
    standard_scaler: bool,
    min_max_scaler: bool):
    """The function load the input dataset and save the normalized version"""

    if standard_scaler is min_max_scaler:
        raise ValueError(
            'Exactly one of standard_scaler or min_max_scaler must be True.')

    with open(input_dataset.path) as f:
        df = pd.read_csv(f)
        labels = df.pop('Labels')

    if standard_scaler:
        scaler = StandardScaler()
    if min_max_scaler:
        scaler = MinMaxScaler()

    df = pd.DataFrame(scaler.fit_transform(df))
    df['Labels'] = labels
    with open(normalized_dataset.path, 'w') as f:
        df.to_csv(f)