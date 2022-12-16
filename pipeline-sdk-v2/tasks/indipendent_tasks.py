from kfp import dsl

# In the following example, my_task1 and my_task2 have no dependency and will execute at the same time.

@dsl.pipeline()
def my_pipeline():
    my_task1 = concat_comp(prefix='hello, ', text='world')
    my_task2 = concat_comp(prefix='hi, ', text='universe')