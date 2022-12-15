import kfp
import kfp.components as comp
import glob
import pandas as pd
import tarfile
import urllib.request
    
# This example builds a Python function-based component
# The function’s arguments are decorated with the kfp.components.InputPath and the kfp.components.OutputPath annotations. 
# These annotations let Kubeflow Pipelines know to provide the path to the zipped tar file, 
# and to create a path where your function stores the merged CSV file.
def merge_csv(file_path: comp.InputPath('Tarball'), 
             output_csv: comp.OutputPath('CSV')):
    """ The function extracts the CSV files and then merges them into a single file """

    # Python function-based components require standalone Python functions. 
    # This means that any required import statements must be defined within the function, 
    # and any helper functions must be defined within the function. 
    import glob
    import pandas as pd
    import tarfile

    tarfile.open(name=file_path, mode="r|gz").extractall('data')
    df = pd.concat([pd.read_csv(csv_file, header=None) for csv_file in glob.glob('data/*.csv')])
    df.to_csv(output_csv, index=False, header=False)

# Use kfp.components.create_component_from_func to return a factory function that you can use to create pipeline steps
create_step_merge_csv = kfp.components.create_component_from_func(
    func=merge_csv,
    output_component_file='component.yaml', # Path to save the component specification to
    base_image='python:3.7', # It specifies the base container image to run this function in
    packages_to_install=['pandas==1.1.4']) # List of PyPI packages that need to be installed in the container at runtime

# Use kfp.components.load_component_from_url to load the component specification YAML for any components that you are reusing in this pipeline.
web_downloader_op = kfp.components.load_component_from_url(
    'https://raw.githubusercontent.com/kubeflow/pipelines/master/components/contrib/web/Download/component.yaml')

# Define the pipeline as a python function
# Create tasks from the previously defined components
def my_pipeline(url):
  web_downloader_task = web_downloader_op(url=url)
  merge_csv_task = create_step_merge_csv(file=web_downloader_task.outputs['data']) # The inputs to the component factory functions can be pipeline parameters, the outputs of other tasks, or a constant value
  # The outputs of the merge_csv_task can be referenced using the
  # merge_csv_task.outputs dictionary: merge_csv_task.outputs['output_csv']

# Compile and run your pipeline

# Option 1: Compile and then upload in UI 
# Run the following to compile your pipeline and save it as pipeline.yaml
kfp.compiler.Compiler().compile(
    pipeline_func=my_pipeline,
    package_path='pipeline.yaml')
# Upload and run your pipeline.yaml using the Kubeflow Pipelines user interface

# Option 2: run the pipeline using Kubeflow Pipelines SDK client
# Create an instance of the kfp.Client class
#client = kfp.Client() # change arguments accordingly
# Run the pipeline using the kfp.Client instance:
#client.create_run_from_pipeline_func(
    #my_pipeline,
    #arguments={
        #'url': 'https://storage.googleapis.com/ml-pipeline-playground/iris-csv-files.tar.gz'
    #})







