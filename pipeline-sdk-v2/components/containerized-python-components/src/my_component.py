# my_component.py
from kfp import dsl
from tensorflow import keras
from .my_helper_module import compile_and_train, get_model, split_dataset # The component uses functions defined in my_helper_module imported via a relative import
# Notice that most of the logic is extracted into helper functions in my_helper_module, permitting a cleaner, modular component function

@dsl.component(
    base_image='python:3.7',
    target_image='gcr.io/my-project/my-component:v1', # The @kfp.dsl.component decorator is given a target_image
    packages_to_install=['tensorflow'],
)
def train_model(
    dataset: Input[Dataset],
    model: Output[Model],
    num_epochs: int,
):
    # load and process the Dataset artifact
    with open(dataset.path) as f:
        x, y = split_dataset(f)

    untrained_model = get_model()

    # train for num_epochs
    trained_model = compile_and_train(untrained_model, epochs=num_epochs)

    # save the Model artifact
    trained_model.save(model.path)

# The my_component.py module, the my_helper_module.py module, and any other source code files you wish to include in the container image should be grouped together in a directory. 
# When you build the component in Step 2 below, this directory will by COPY’d into the image:

# src/
# ├── my_component.py
# └── my_helper_module.py
# └── another_module.py

# You can use the KFP CLI to build your component
# include the --push-image flag to push your image to a remote registry from which the executing backend can pull your image at runtime.

# kfp component build src/ --push-image

# When to use? Containerized Python components should be used any time your component is implemented as Python code, 
# but cannot be written as a standalone Python function or you wish to organize source code outside of the component Python function definition.

