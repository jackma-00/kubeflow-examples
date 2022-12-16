from kfp import components

load_dataset_component = components.load_component_from_file('src/component_metadata/load_dataset.yaml')