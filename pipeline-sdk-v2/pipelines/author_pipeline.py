from kfp import dsl

# Pipelines are defined using Python pipeline functions decorated with @dsl.pipeline

@dsl.pipeline(
    name='example-pipeline',
    description='This pipeline wants to be an example on how to author a pipeline'
)
def my_pipeline(text: str):
    # a pipeline instantiates components as tasks and uses them to form a computational graph
    my_task = my_component(arg1=text)

# Within the scope of a pipeline, control flow acts on tasks, is authored using DSL features, and is executed by the KFP backend through the creation of Kubernetes Pods to execute those tasks. 
# dsl.Condition, dsl.ParallelFor and dsl.ExitHandler can be used to orchestrate the completion of tasks within a pipeline function body. 
# Each is implemented as a Python context manager.

