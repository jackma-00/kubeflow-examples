import kfp
from kfp.components import InputPath, OutputPath, create_component_from_func

def train(test_samples_fraction: float,
          seed: int,
          results: OutputPath('results')):
    """The function train a model and outputs the predictions."""

    import pandas as pd
    from sklearn import model_selection
    from sklearn.linear_model import LogisticRegression
    from sklearn import datasets

    # Load iris dataset
    iris = datasets.load_iris()

    # Create feature matrix
    X = iris.data

    # Create target vector
    y = iris.target

    # Split data
    X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=test_samples_fraction, random_state=seed)

    # Model instance
    model = LogisticRegression()
    
    # Fit model
    model.fit(X_train, y_train)

    # Predict 
    y_pred = model.predict(X_test)

    test_prediction_results = pd.DataFrame(data={'y_test':y_test, 'y_pred':y_pred}).reset_index(drop=True)
    test_prediction_results.to_csv(results, index=False)

def evaluate(test_results: InputPath('results'),
             mlpipeline_metrics: OutputPath('Metrics')):
    """The function evaluates the model performance."""

    import json
    import pandas as pd
    from sklearn.metrics import accuracy_score

    def classification_metrics_helper(df):

        accuracy = accuracy_score(df["y_test"], df["y_pred"])
        
        metrics={
          'metrics': [{
          'name': 'accuracy-score', # The name of the metric. Visualized as the column name in the runs table.
          'numberValue': accuracy, # The value of the metric. Must be a numeric value.
          'format': "PERCENTAGE"   # The optional format of the metric. Supported values are "RAW" (displayed in raw format) and "PERCENTAGE" (displayed in percentage format).
          }]
        }
      
        return metrics


    df = pd.read_csv(test_results)
    metrics = classification_metrics_helper(df)
    with open(mlpipeline_metrics, 'w') as f:
        json.dump(metrics, f)

train_op = create_component_from_func(
    func=train,
    base_image='python:3.8',
    packages_to_install=['pandas', 'scikit-learn'],
    output_component_file='train_component.yaml'
)

evaluate_op = create_component_from_func(
    func=evaluate,
    base_image='python:3.8',
    packages_to_install=['pandas', 'scikit-learn'],
    output_component_file='evaluate_component.yaml'
)

def train_evaluation_pipeline():
  train_task = train_op(test_samples_fraction=0.3, seed=7)
  evaluate_task = evaluate_op(test_results=train_task.outputs['results'])

if __name__ == '__main__':
    # Compiling the pipeline
    kfp.compiler.Compiler().compile(
    pipeline_func=train_evaluation_pipeline,
    package_path='train_evaluation_pipeline.yaml')