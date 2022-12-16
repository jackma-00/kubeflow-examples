from kfp import dsl

# The dsl.ParallelFor context manager allows parallelized execution of tasks over a static set of items. 

# In the following pipeline, train_model will train a model for 1, 5, 10, and 25 epochs, with no more than two training tasks running at one time:

@dsl.pipeline
def my_pipeline():
    with dsl.ParallelFor(
        items=[1, 5, 10, 25],
        parallelism=2
    ) as epochs:
        train_model(epochs=epochs)