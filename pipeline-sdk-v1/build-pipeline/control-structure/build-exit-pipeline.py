# # DSL control structures tutorial
# Shows how to use conditional execution and exit handlers.

from typing import NamedTuple

import kfp
from kfp import dsl
from kfp.components import func_to_container_op, InputPath, OutputPath

# ## Conditional execution
# You can use the `with dsl.Condition(task1.outputs["output_name"] = "value"):` context to execute parts of the pipeline conditionally

@func_to_container_op
def get_random_int_op(minimum: int, maximum: int) -> int:
    """Generate a random number between minimum and maximum (inclusive)."""
    import random
    result = random.randint(minimum, maximum)
    print(result)
    return result

@func_to_container_op
def flip_coin_op() -> str:
    """Flip a coin and output heads or tails randomly."""
    import random
    result = random.choice(['heads', 'tails'])
    print(result)
    return result

@func_to_container_op
def print_op(message: str):
    """Print a message."""
    print(message)

@func_to_container_op
def fail_op(message):
    """Fails."""
    import sys
    print(message)    
    sys.exit(1)
    
# ## Exit handlers
# You can use `with dsl.ExitHandler(exit_task):` context to execute a task when the rest of the pipeline finishes (succeeds or fails)

@dsl.pipeline(
    name='Conditional execution pipeline with exit handler',
    description='Shows how to use dsl.Condition() and dsl.ExitHandler().'
)
def flipcoin_exit_pipeline():
    exit_task = print_op('Exit handler has worked!')
    with dsl.ExitHandler(exit_task):
        flip = flip_coin_op()
        with dsl.Condition(flip.output == 'heads'):
            random_num_head = get_random_int_op(0, 9)
            with dsl.Condition(random_num_head.output > 5):
                print_op('heads and %s > 5!' % random_num_head.output)
            with dsl.Condition(random_num_head.output <= 5):
                print_op('heads and %s <= 5!' % random_num_head.output)

        with dsl.Condition(flip.output == 'tails'):
            random_num_tail = get_random_int_op(10, 19)
            with dsl.Condition(random_num_tail.output > 15):
                print_op('tails and %s > 15!' % random_num_tail.output)
            with dsl.Condition(random_num_tail.output <= 15):
                print_op('tails and %s <= 15!' % random_num_tail.output)

        with dsl.Condition(flip.output == 'tails'):
            fail_op(message="Failing the run to demonstrate that exit handler still gets executed.")

if __name__ == '__main__':
    # Compiling the pipeline
    kfp.compiler.Compiler().compile(
    pipeline_func=flipcoin_exit_pipeline,
    package_path='flipcoin_exit_pipeline.yaml')