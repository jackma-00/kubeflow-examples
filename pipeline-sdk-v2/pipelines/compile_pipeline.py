from kfp import compiler
from kfp import dsl

# Define a simple pipeline

@dsl.component
def addition_component(num1: int, num2: int) -> int:
  return num1 + num2

@dsl.pipeline(name='addition-pipeline')
def my_pipeline(a: int, b: int, c: int = 10):
  add_task_1 = addition_component(num1=a, num2=b)
  add_task_2 = addition_component(num1=add_task_1.output, num2=c)

# Compile the pipeline to the file my_pipeline.yaml
cmplr = compiler.Compiler()
cmplr.compile(my_pipeline, package_path='my_pipeline.yaml')

# Compile the component addition_component to the file addition_component.yaml
cmplr.compile(addition_component, package_path='addition_component.yaml')