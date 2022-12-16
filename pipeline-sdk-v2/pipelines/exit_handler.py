from kfp import dsl

# The dsl.ExitHandler context manager allows pipeline authors to specify an “exit handler” task which will run after the tasks within its scope finish execution or one of them fails.

# In the following pipeline, clean_up_task will execute after either both create_dataset and train_and_save_models finish or one of them fails:

@dsl.pipeline
def my_pipeline():
    clean_up_task = clean_up_resources()
    with dsl.ExitHandler(exit_task=clean_up_task):
        dataset_task = create_datasets()
        train_task = train_and_save_models(dataset=dataset_task.output)