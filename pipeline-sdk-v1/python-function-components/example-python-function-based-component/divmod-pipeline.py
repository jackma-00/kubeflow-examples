from typing import NamedTuple
import kfp
from kfp.components import create_component_from_func
import kfp.dsl as dsl

# Define divmod function
def my_divmod(
  dividend: float,
  divisor: float) -> NamedTuple(
    'MyDivmodOutput',
    [
      ('quotient', float),
      ('remainder', float),
      ('mlpipeline_ui_metadata', 'UI_metadata'),
      ('mlpipeline_metrics', 'Metrics')
    ]):
    '''Divides two numbers and calculate  the quotient and remainder'''

    # Import the numpy package inside the component function
    import numpy as np

    # Define a helper function
    def divmod_helper(dividend, divisor):
        return np.divmod(dividend, divisor)

    (quotient, remainder) = divmod_helper(dividend, divisor)

    from tensorflow.python.lib.io import file_io
    import json

    # Export a sample tensorboard
    metadata = {
      'outputs' : [{
        'type': 'tensorboard',
        'source': 'gs://ml-pipeline-dataset/tensorboard-train',
      }]
    }

    # Export two metrics
    metrics = {
      'metrics': [{
          'name': 'quotient',
          'numberValue':  float(quotient),
        },{
          'name': 'remainder',
          'numberValue':  float(remainder),
        }]}

    from collections import namedtuple
    divmod_output = namedtuple('MyDivmodOutput',
        ['quotient', 'remainder', 'mlpipeline_ui_metadata',
         'mlpipeline_metrics'])
    return divmod_output(quotient, remainder, json.dumps(metadata),
                         json.dumps(metrics))
                    
# Define add function
def add(a: float, b: float) -> float:
    '''Calculates sum of two arguments'''
    return a + b

# Create divmod factory function
divmod_op = create_component_from_func(
    my_divmod, base_image='tensorflow/tensorflow:1.11.0-py3',
    output_component_file='divmod_component.yaml')

# Create add factory function
add_op = create_component_from_func(
    add, output_component_file='add_component.yaml')

# Define the pipeline
import kfp.dsl as dsl
@dsl.pipeline(
   name='Calculation pipeline',
   description='An example pipeline that performs arithmetic calculations.'
)
def calc_pipeline(
   a='1',
   b='7',
   c='17',
):
    # Passes a pipeline parameter and a constant value as operation arguments.
    add_task = add_op(a, 4) # The add_op factory function returns
                            # a dsl.ContainerOp class instance. 

    # Passes the output of the add_task and a pipeline parameter as operation
    # arguments. For an operation with a single return value, the output
    # reference is accessed using `task.output` or
    # `task.outputs['output_name']`.
    divmod_task = divmod_op(add_task.output, b)

    # For an operation with multiple return values, output references are
    # accessed as `task.outputs['output_name']`.
    result_task = add_op(divmod_task.outputs['quotient'], c)

    # Compile and run your pipeline

# Option 1: Compile and then upload in UI 
# Run the following to compile your pipeline and save it as pipeline.yaml
kfp.compiler.Compiler().compile(
    pipeline_func=calc_pipeline,
    package_path='pipeline.yaml')
# Upload and run your pipeline.yaml using the Kubeflow Pipelines user interface