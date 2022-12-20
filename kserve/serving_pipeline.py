from typing import List

import kfp
from kfp import Client
from kfp import compiler
from kfp.v2 import dsl
from kfp.v2.dsl import Dataset, Input, Model, Output

from auth_helper import get_istio_auth_session

KUBEFLOW_ENDPOINT = "http://localhost:8080"
KUBEFLOW_USERNAME = "user@example.com"
KUBEFLOW_PASSWORD = "12341234"
KUBEFLOW_NAMESPACE = "kubeflow-user-example-com"

@dsl.component(packages_to_install=['pandas==1.3.5'])
def create_dataset(iris_dataset: Output[Dataset]):
    import pandas as pd

    csv_url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data'
    col_names = [
        'Sepal_Length', 'Sepal_Width', 'Petal_Length', 'Petal_Width', 'Labels'
    ]
    df = pd.read_csv(csv_url, names=col_names)

    with open(iris_dataset.path, 'w') as f:
        df.to_csv(f)


@dsl.component(packages_to_install=['pandas==1.3.5', 'scikit-learn==1.0.2'])
def normalize_dataset(
    input_iris_dataset: Input[Dataset],
    normalized_iris_dataset: Output[Dataset],
    standard_scaler: bool,
    min_max_scaler: bool,
):
    if standard_scaler is min_max_scaler:
        raise ValueError(
            'Exactly one of standard_scaler or min_max_scaler must be True.')

    import pandas as pd
    from sklearn.preprocessing import MinMaxScaler
    from sklearn.preprocessing import StandardScaler

    with open(input_iris_dataset.path) as f:
        df = pd.read_csv(f)
    labels = df.pop('Labels')

    if standard_scaler:
        scaler = StandardScaler()
    if min_max_scaler:
        scaler = MinMaxScaler()

    df = pd.DataFrame(scaler.fit_transform(df))
    df['Labels'] = labels
    with open(normalized_iris_dataset.path, 'w') as f:
        df.to_csv(f)


@dsl.component(packages_to_install=['pandas==1.3.5', 'scikit-learn==1.0.2'])
def train_model(
    normalized_iris_dataset: Input[Dataset],
    model: Output[Model],
    n_neighbors: int,
):
    import pickle

    import pandas as pd
    from sklearn.model_selection import train_test_split
    from sklearn.neighbors import KNeighborsClassifier

    with open(normalized_iris_dataset.path) as f:
        df = pd.read_csv(f)

    y = df.pop('Labels')
    X = df

    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

    clf = KNeighborsClassifier(n_neighbors=n_neighbors)
    clf.fit(X_train, y_train)
    with open(model.path, 'wb') as f:
        pickle.dump(clf, f)

@dsl.component(packages_to_install=['kubernetes', 'kserve'])
def serve_model(model: Input[Model]):

    from kubernetes import client 
    from kserve import KServeClient
    from kserve import constants
    from kserve import utils
    from kserve import V1beta1InferenceService
    from kserve import V1beta1InferenceServiceSpec
    from kserve import V1beta1PredictorSpec
    from kserve import V1beta1SKLearnSpec

    # Adapt model uri to a s3 compatible one 
    model_uri = model.path.replace('/minio/', 's3://')

    # This will retrieve the current namespace of your Kubernetes context. The InferenceService will be deployed in this namespace.
    namespace = utils.get_default_target_namespace()

    # Define the inference service
    name='iris-knn-predictor'
    kserve_version='v1beta1'
    api_version = constants.KSERVE_GROUP + '/' + kserve_version

    isvc = V1beta1InferenceService(api_version=api_version,
                                   kind=constants.KSERVE_KIND,
                                   metadata=client.V1ObjectMeta(
                                        name=name, namespace=namespace, annotations={'sidecar.istio.io/inject':'false'}),
                                   spec=V1beta1InferenceServiceSpec(
                                   predictor=V1beta1PredictorSpec(
                                   sklearn=(V1beta1SKLearnSpec(
                                        storage_uri=model_uri))))
    )

    # Create the inference service
    KServe = KServeClient()
    KServe.create(isvc)

@dsl.pipeline(name='serving-pipeline', 
              description='This pipeline wants to test KServe feature')
def serving_pipeline(
    standard_scaler: bool,
    min_max_scaler: bool,
    neighbors: int,
):
    create_dataset_task = create_dataset()

    normalize_dataset_task = normalize_dataset(
        input_iris_dataset=create_dataset_task.outputs['iris_dataset'],
        standard_scaler=True,
        min_max_scaler=False)

    train_model_task = train_model(normalized_iris_dataset=normalize_dataset_task.outputs['normalized_iris_dataset'],
        n_neighbors=neighbors)

    serve_model_task = serve_model(model=train_model_task.outputs['model'])


auth_session = get_istio_auth_session(
    url=KUBEFLOW_ENDPOINT,
    username=KUBEFLOW_USERNAME,
    password=KUBEFLOW_PASSWORD
)

kfp_client = Client(host=f"{KUBEFLOW_ENDPOINT}/pipeline", cookies=auth_session["session_cookie"])

cmplr = compiler.Compiler(mode=kfp.dsl.PipelineExecutionMode.V2_COMPATIBLE)
cmplr.compile(serving_pipeline, package_path='serving_pipeline.yaml')

# To submit IR YAML for execution use the .create_run_from_pipeline_package method:
kfp_client.create_run_from_pipeline_package(
    pipeline_file='serving_pipeline.yaml',
    arguments={
        'min_max_scaler': True,
        'standard_scaler': False,
        'neighbors': 3
    },
    experiment_name='ML Related Experiments',
    namespace=KUBEFLOW_NAMESPACE)