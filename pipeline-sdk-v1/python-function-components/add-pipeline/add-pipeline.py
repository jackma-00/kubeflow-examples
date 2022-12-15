import kfp
from kfp.components import create_component_from_func
import kfp.dsl as dsl

# Define your component’s code as a standalone Python function
def add(a: float, b: float) -> float:
    '''Calculates sum of two arguments'''
    return a + b

# Use kfp.components.create_component_from_func to generate the component specification YAML and, 
# return a factory function that you can use to create kfp.dsl.ContainerOp class instances for your pipeline
add_op = create_component_from_func(
    add, output_component_file='add_component.yaml')

# Create and run your pipeline
import kfp.dsl as dsl
@dsl.pipeline(
  name='Addition pipeline',
  description='An example pipeline that performs addition calculations.'
)
def add_pipeline(
  a='1',
  b='7',
):
  # Passes a pipeline parameter and a constant value to the `add_op` factory
  # function.
  first_add_task = add_op(a, 4)
  # Passes an output reference from `first_add_task` and a pipeline parameter
  # to the `add_op` factory function. For operations with a single return
  # value, the output reference can be accessed as `task.output` or
  # `task.outputs['output_name']`.
  second_add_task = add_op(first_add_task.output, b)

# Specify argument values for your pipeline run.
#arguments = {'a': 7, 'b': 8}

# Compile and run your pipeline

# Option 1: Compile and then upload in UI 
# Run the following to compile your pipeline and save it as pipeline.yaml
kfp.compiler.Compiler().compile(
    pipeline_func=add_pipeline,
    package_path='pipeline.yaml')
# Upload and run your pipeline.yaml using the Kubeflow Pipelines user interface



