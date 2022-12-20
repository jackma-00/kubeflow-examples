import requests

EXTERNAL_URL = 'http://iris-knn-predictor.kubeflow-user-example-com.example.com'

inference_input = {
  'instances': [
    [6.8,  2.8,  4.8,  1.4],
    [6.0,  3.4,  4.5,  1.6]
  ]
}

response = requests.post(url=EXTERNAL_URL, json=inference_input)
print(response.text)