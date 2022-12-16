from kfp import dsl

# The dsl.Condition context manager allows conditional execution of tasks within its scope based on the output of an upstream task. 

@dsl.pipeline
def my_pipeline():
    coin_flip_task = flip_coin()
    with dsl.Condition(coin_flip_task.output == 'heads'):
        conditional_task = my_comp()