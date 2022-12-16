from typing import List
import kfp
from kfp.v2 import dsl
from kfp import components
from kfp import compiler

# Relative paths to the component's specs 
LOAD_DATASET_PATH = '../../components/data/load-dataset/src/component_metadata/load_dataset.yaml'
NORMALIZE_DATASET_PATH = '../../components/data/normalize-dataset/src/component_metadata/normalize_dataset.yaml'
TRAIN_KNN_PATH = '../../components/models/knn/src/component_metadata/train_knn.yaml'

# Load components from file
load_dataset_component = components.load_component_from_file(LOAD_DATASET_PATH)
normalize_dataset_component = components.load_component_from_file(NORMALIZE_DATASET_PATH)
train_knn_component = components.load_component_from_file(TRAIN_KNN_PATH)


# Define the pipeline
@dsl.pipeline(
    name='knn-training-pipeline',
    description='This pipeline wants to be an example pipeline training a knn model')
def knn_training_pipeline(
    standard_scaler: bool,
    min_max_scaler: bool,
    neighbors: List[int],
):
    load_dataset_task = load_dataset_component()

    normalize_dataset_task = normalize_dataset_component(
        input_dataset=load_dataset_task.outputs['dataset'],
        standard_scaler=True,
        min_max_scaler=False)

    with dsl.ParallelFor(neighbors) as n_neighbors:
        train_knn_component(
            normalized_dataset=normalize_dataset_task
            .outputs['normalized_dataset'],
            n_neighbors=n_neighbors)

# Compile the pipeline
cmplr = compiler.Compiler(mode=kfp.dsl.PipelineExecutionMode.V2_COMPATIBLE)
cmplr.compile(pipeline_func=knn_training_pipeline, package_path='knn_training_pipeline.yaml')