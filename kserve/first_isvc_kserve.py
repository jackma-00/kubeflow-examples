from kubernetes import client 
from kserve import KServeClient
from kserve import constants
from kserve import utils
from kserve import V1beta1InferenceService
from kserve import V1beta1InferenceServiceSpec
from kserve import V1beta1PredictorSpec
from kserve import V1beta1SKLearnSpec

KUBEFLOW_NAMESPACE = 'ML Related Experiments' # Current namespace of your Kubernetes context. The InferenceService will be deployed in this namespace.
KUBE_CONFIG_FILE = 'config_file' # Name (path) of the kube-config file.

# Instantiate the client 
KServe = KServeClient(config_file=KUBE_CONFIG_FILE)
KServe.set_credentials()

# Define the inference service 
name='sklearn-iris'
kserve_version='v1beta1'
api_version = constants.KSERVE_GROUP + '/' + kserve_version

isvc = V1beta1InferenceService(api_version=api_version,
                               kind=constants.KSERVE_KIND,
                               metadata=client.V1ObjectMeta(
                                   name=name, namespace=KUBEFLOW_NAMESPACE, annotations={'sidecar.istio.io/inject':'false'}),
                               spec=V1beta1InferenceServiceSpec(
                               predictor=V1beta1PredictorSpec(
                               sklearn=(V1beta1SKLearnSpec( # an embedded V1beta1SKLearnSpec object is created
                                   storage_uri="gs://kfserving-samples/models/sklearn/iris")))) # a storage URI is provided, pointing to the location of the trained iris model in cloud storage.
)

# Create the inference service 

KServe.create(isvc)

# Check the inference service
KServe.get(name, namespace=KUBEFLOW_NAMESPACE, watch=True, timeout_seconds=120)