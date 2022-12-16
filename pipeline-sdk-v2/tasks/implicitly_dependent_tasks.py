from kfp import dsl

# When the output of one task is the input to another, an implicit dependency is created between the two tasks.

@dsl.pipeline()
def my_pipeline():
    my_task1 = concat_comp(prefix='hello, ', text='world')
    my_task2 = concat_comp(prefix=my_task1.output, text='!') # This means my_task2 implicitly depends and will execute after my_task1.