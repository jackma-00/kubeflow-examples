from kfp import dsl
from kfp.dsl import Dataset, Input, Model, Output

@dsl.component
def train_model(dataset: Input[Dataset], model: Output[Model]):
    # do training
    trained_model = ...
    trained_model.save(model.path)

# the training_workflow pipeline returns a Model from the inner train_model component

@dsl.pipeline
def training_workflow() -> Model:
    get_dataset_op = get_dataset()
    train_model_op = train_model(dataset=get_dataset_op.outputs['dataset'])
    return train_model_op.outputs['model']