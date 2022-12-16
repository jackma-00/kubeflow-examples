from kfp.dsl import (
  container_component,
  ContainerSpec,
  Dataset,
  Input,
  pipeline,
  Output,
) 

# Write your component’s code as a Python function that returns a dsl.ContainerSpec object to specify the container image 
# and the commands to be run in the container and wrap the function into a @container_component decorator
@container_component
def create_dataset(text: str, output_gcs: Output[Dataset]): # Specify your function’s inputs and outputs in the function’s signature
    return ContainerSpec(
        image='alpine',
        command=[
            'sh',
            '-c',
            'mkdir --parents $(dirname "$1") && echo "$0" > "$1"',
        ],
        args=[text, output_gcs.path]) # It’s recommended to place the input of the components in the args section instead of the command section


@container_component
def print_dataset(input_gcs: Input[Dataset]):
    return ContainerSpec(image='alpine', command=['cat'], args=[input_gcs.path])

# Below is an example that authors a pipelines from two custom container components.
@pipeline
def two_step_pipeline_containerized(text: str):
    create_dataset_task = create_dataset(text)
    print_dataset_task = print_dataset(input_gcs=create_dataset_task.outputs['output_gcs'])

# In the above example, the create_dataset component takes in a text and output it to a path as an artifact. 
# Then, the print_dataset component retrieves the artifact output by the create_dataset component and prints it out