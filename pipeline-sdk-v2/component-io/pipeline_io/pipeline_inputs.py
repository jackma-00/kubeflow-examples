from kfp import dsl
from kfp.dsl import Input, Output, Dataset

# All pipeline inputs must include type annotations. Valid input parameter annotations include str, int, float, bool, dict, list.
# The only valid input artifact annotation is Input[<Artifact>] (where <Artifact> is any KFP-compatible artifact class). 

@dsl.pipeline
def my_pipeline(text: str, number: int = 10):
    # Ultimately, all inputs must be passed to an inner “primitive” component in order to perform computation on the input. 
    ...