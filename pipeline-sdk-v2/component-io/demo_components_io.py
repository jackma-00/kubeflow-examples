from kfp import dsl
from kfp.dsl import Input, Output, Dataset


@dsl.container_component
def create_dataset(
    initial_text: str, # input parameter
    output_dataset: Output[Dataset], # output artifact
):
    """Create a dataset containing the string `initial_text`.""" 
    return dsl.ContainerSpec(
        image='alpine',
        command=['sh', '-c', 'mkdir --parents $(dirname "$1") && echo "$0" > "$1"',],
        args=[initial_text, output_dataset.path])


@dsl.component
def augment_dataset(
    existing_dataset: Input[Dataset], # input artifact 
    resulting_dataset: Output[Dataset], # output artifact
    text: str, # input parameter
    num: int = 10, # input parameter
) -> int: # output parameter 
    """Append `text` `num` times to an existing dataset, then write it as a new dataset."""
    additional_data = ' '.join(text for _ in range(num))

    # .path method, which can be used to access the local path where the artifact file has been copied
    with open(existing_dataset.path, 'r') as f:
        existing_dataset_text = f.read()

    resulting_dataset_text = existing_dataset_text + ' ' + additional_data

    # As with using an artifact input, component authors should write artifacts to .path:
    with open(resulting_dataset.path, 'w') as f:
        f.write(resulting_dataset_text)
    # At run time output artifacts are copied to remote storage from the .path

    return len(resulting_dataset_text)


@dsl.pipeline()
def my_pipeline(initial_text: str = 'initial dataset text'):
    create_task = create_dataset(initial_text=initial_text)
    augment_dataset(
        existing_dataset=create_task.outputs['output_dataset'], # we pass the output_dataset from create_dataset to existing_dataset parameters
        text='additional text')
    # When the augment_dataset component runs, 
    # the executing backend copies the output_dataset artifact file to the container filesystem, 
    # and passes in an instance of Dataset as an argument to existing_dataset