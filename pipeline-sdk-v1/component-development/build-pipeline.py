import kfp
import kfp.components as comp

create_step_get_lines = comp.load_component_from_text("""
name: Get Lines
description: Gets the specified number of lines from the input file.

inputs:
- {name: Input 1, type: String, description: 'Data for input 1'}
- {name: Parameter 1, type: Integer, default: '100', description: 'Number of lines to copy'}

outputs:
- {name: Output 1, type: String, description: 'Output 1 data.'}

implementation:
  container:
    # The strict name of a container image that you've pushed to a container registry.
    image: jackma00/component-development-test
    # command is a list of strings (command-line arguments). 
    # The YAML language has two syntaxes for lists and you can use either of them. 
    # Here we use the "flow syntax" - comma-separated strings inside square brackets.
    command: [
      python3, 
      # Path of the program inside the container
      /pipelines/component/src/program.py,
      --input1-path,
      {inputPath: Input 1},
      --param1, 
      {inputValue: Parameter 1},
      --output1-path, 
      {outputPath: Output 1},
    ]""")

# create_step_get_lines is a "factory function" that accepts the arguments
# for the component's inputs and output paths and returns a pipeline step
# (ContainerOp instance).
#
# To inspect the get_lines_op function in Jupyter Notebook, enter 
# "get_lines_op(" in a cell and press Shift+Tab.
# You can also get help by entering `help(get_lines_op)`, `get_lines_op?`,
# or `get_lines_op??`.

# Create a simple component using only bash commands. The output of this component
# can be passed to a downstream component that accepts an input with the same type.
create_step_write_lines = comp.load_component_from_text("""
name: Write Lines
description: Writes text to a file.

inputs:
- {name: text, type: String}

outputs:
- {name: data, type: String}

implementation:
  container:
    image: busybox
    command:
    - sh
    - -c
    - |
      mkdir -p "$(dirname "$1")"
      echo "$0" > "$1"
    args:
    - {inputValue: text}
    - {outputPath: data}
""")

# Define your pipeline 
def my_pipeline():
    write_lines_step = create_step_write_lines(
        text='one\ntwo\nthree\nfour\nfive\nsix\nseven\neight\nnine\nten')

    get_lines_step = create_step_get_lines(
        # Input name "Input 1" is converted to pythonic parameter name "input_1"
        input_1=write_lines_step.outputs['data'],
        parameter_1=5,
    )

# Compile and run your pipeline

# Option 1: Compile and then upload in UI 
# Run the following to compile your pipeline and save it as pipeline.yaml
kfp.compiler.Compiler().compile(
    pipeline_func=my_pipeline,
    package_path='pipeline.yaml')
# Upload and run your pipeline.yaml using the Kubeflow Pipelines user interface

# If you run this command on a Jupyter notebook running on Kubeflow,
# you can exclude the host parameter.
# client = kfp.Client()
#client = kfp.Client(host='<your-kubeflow-pipelines-host-name>')

# Compile, upload, and submit this pipeline for execution.
#client.create_run_from_pipeline_func(my_pipeline, arguments={})