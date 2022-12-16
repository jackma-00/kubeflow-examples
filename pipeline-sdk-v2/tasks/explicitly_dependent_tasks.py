from kfp import dsl

# Sometimes you want to order execution of two tasks but not pass data between the tasks. 
# When this is the case, you can call the intended second task’s .after() on the intended first task create an explicit dependency. 

@dsl.pipeline()
def my_pipeline():
    my_task1 = concat_comp(prefix='hello, ', text='world')
    my_task2 = concat_comp(prefix='hi, ', text='universe').after(my_task1)