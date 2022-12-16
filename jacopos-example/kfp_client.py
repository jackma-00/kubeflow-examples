import kfp
from auth_helper import get_istio_auth_session

# Session parameters 
KUBEFLOW_ENDPOINT = "http://localhost:8080"
KUBEFLOW_USERNAME = "user@example.com"
KUBEFLOW_PASSWORD = "12341234"
KUBEFLOW_NAMESPACE = "kubeflow-user-example-com"

# Relative path to the pipeline's spec 
PIPELINE_FILE = 'pipelines/knn-pipeline/knn_training_pipeline.yaml'

# Experiment's information 
EXPERIMENT_NAME = 'ML Related Experiments'

# Retrieve cookies from Kubeflow Central Dashboard Session
auth_session = get_istio_auth_session(
    url=KUBEFLOW_ENDPOINT,
    username=KUBEFLOW_USERNAME,
    password=KUBEFLOW_PASSWORD
)

# Instantiate client
client = kfp.Client(host=f"{KUBEFLOW_ENDPOINT}/pipeline", cookies=auth_session["session_cookie"])

# Submit IR YAML for execution
client.create_run_from_pipeline_package(
    pipeline_file=PIPELINE_FILE,
    arguments={
        'min_max_scaler': True,
        'standard_scaler': False,
        'neighbors': [3, 6, 9]
    },
    experiment_name=EXPERIMENT_NAME,
    namespace=KUBEFLOW_NAMESPACE)