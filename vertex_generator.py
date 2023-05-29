from google.cloud import aiplatform
from google.cloud.aiplatform.gapic.schema import predict
from google.protobuf import json_format
from google.protobuf.struct_pb2 import Value


class GeneratorBase:
    def generate(self, query: str, parameters: dict) -> str:
        raise NotImplementedError

    def __call__(self, query: str, parameters: dict = None) -> str:
        return self.generate(query, parameters)


class VertexGenerator(GeneratorBase):
    def __init__(self, project_id, model_name, location):
        self.project_id = project_id
        self.model_name = model_name
        self.location = location
        self.api_endpoint = f"{self.location}-aiplatform.googleapis.com"
        self.endpoint = f"projects/{self.project_id}/locations/{self.location}/publishers/google/models/{self.model_name}"

    def generate(self, query: str, parameters: dict = None) -> str:
        # The AI Platform services require regional API endpoints.
        client_options = {"api_endpoint": self.api_endpoint}
        # Initialize client that will be used to create and send requests.
        client = aiplatform.gapic.PredictionServiceClient(client_options=client_options)

        # Prepare instance
        instance_dict = {"prefix": query}
        instance = json_format.ParseDict(instance_dict, Value())
        instances = [instance]

        # If parameters are not supplied, use default
        if parameters is None:
            parameters = {
                "temperature": 0.2,
                "maxOutputTokens": 256
            }
        else:
            if 'max_new_tokens' in parameters:
                # Convert 'max_new_tokens' to 'maxOutputTokens'
                parameters['maxOutputTokens'] = parameters.pop('max_new_tokens')

        parameters_dict = parameters
        parameters = json_format.ParseDict(parameters_dict, Value())

        # Perform prediction
        response = client.predict(endpoint=self.endpoint, instances=instances, parameters=parameters)

        # Extract generated text
        generated_text = ""
        predictions = response.predictions
        for prediction in predictions:
            dict_val = dict(prediction)
            generated_text += dict_val['content']

        return generated_text
