import kfp

# submit pipeline runs from the KFP SDK client

client = kfp.Client(host='<YOUR_HOST_URL>')

# To submit IR YAML for execution use the .create_run_from_pipeline_package method:
client.create_run_from_pipeline_package('pipeline.yaml', arguments={'param': 'a', 'other_param': 2})

# To submit a Python pipeline function for execution use the .create_run_from_pipeline_func convenience method, 
# which wraps compilation and run submission into one method:
client.create_run_from_pipeline_func('pipeline.yaml', arguments={'param': 'a', 'other_param': 2})

