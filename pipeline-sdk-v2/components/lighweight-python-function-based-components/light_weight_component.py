from kfp import dsl

# 1. Define a standalone function.
# 2. Include type annotations for the function parameters and return values.
# 3. Decorate your function with the @kfp.dsl.component decorator. 
@dsl.component(
    base_image='python:3.7',
    packages_to_install=['tensorflow==2.9.1'] # Packages will be pip installed at container runtime
)
def train_model(
    dataset: Input[Dataset],
    model: Output[Model],
    num_epochs: int,
):
    """The following is an example of a lightweight component that trains a model on an existing input Dataset artifact for num_epochs epochs, 
    then saves the output Model artifact"""

    # Include all import statements within the function body
    from tensorflow import keras
    
    # load and process the Dataset artifact
    with open(dataset.path) as f:
        x, y = ...

    my_model = keras.Sequential(
        [
            layers.Dense(4, activation='relu', name='layer1'),
            layers.Dense(3, activation='relu', name='layer2'),
            layers.Dense(2, activation='relu', name='layer2'),
            layers.Dense(1, name='layer3'),
        ]
    )

    my_model.compile(...)
    # train for num_epochs
    my_model.fit(x, y, epochs=num_epochs)
    
    # save the Model artifact
    my_model.save(model.path)

# When to use? Lightweight components should be used if your component implementation can be written as a standalone Python function and does not require an abundance of source code. 
# This is the preferred authoring approach for quick demos and when authoring components in a notebook.

# For more involved components and for production usage, prefer containerized components and custom container components for their increased flexibility.

# Note: This authoring approach replaces kfp.components.create_component_from_func in KFP v1.

