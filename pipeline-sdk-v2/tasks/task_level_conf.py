from kfp import dsl

# All task-level configurations are set using a method on the task. 
# Take the following environment variable example:

@dsl.component
def print_env_var():
    import os
    print(os.environ.get('MY_ENV_VAR'))

@dsl.pipeline()
def my_pipeline():
    task = print_env_var()
    task.set_env_variable('MY_ENV_VAR', 'hello')
    # Task-level configuration methods can also be chained:
    #task = print_env_var().set_env_variable('MY_ENV_VAR', 'hello').set_env_variable('OTHER_VAR', 'world')