import requests
import json

from vecflowapi.Pipeline import Pipeline


class Client:
    API_URL = "https://vecflow-apis-2147-e82b72a8-4s59j2od.onporter.run"
    # API_URL = "http://127.0.0.1:5001"
    _api_key = None

    def __init__(self, api_key=None):
        self._api_key = api_key

    def _has_api_key(self):
        return self._api_key is not None

    def _login(self, username, password):
        request_json = {"email_id": username, "password": password}
        response = requests.post(self.API_URL + "/users/login", json=request_json)
        if response.status_code == 200:
            response_data = response.json()
            return response_data["token"]

    def signup(self, username, password):
        request_json = {"email_id": username, "password": password}
        response = requests.post(self.API_URL + "/users/signup", json=request_json)
        if response.status_code == 200:
            print("Success! You have been signed up.")

    def generate_api_key(self, username, password):
        jwt_token = self._login(username, password)

        url = self.API_URL + "/api_keys/generate"
        headers = {
            "accept": "application/json",
            "Authorization": jwt_token,
        }
        response = requests.post(url, headers=headers)
        if response.status_code == 200:
            return response.json()["api_key"]

    def list_api_keys(self, username, password):
        jwt_token = self._login(username, password)

        url = self.API_URL + "/api_keys/"
        headers = {
            "accept": "application/json",
            "Authorization": jwt_token,
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()["api_keys"]

    def create_pipeline(
        self,
        name,
        splitter_type="NLTKTextSplitter",
        splitter_args=None,
        embedder_type="OpenAIEmbedder",
        embedder_args=None,
        vector_store_type="PineconeVectorStore",
        vector_store_args=None,
    ):
        if vector_store_args is None:
            vector_store_args = {
                "api_key": None,
                "environment": "env-name",
                "index": "index-name",
            }
        if embedder_args is None:
            embedder_args = {"api_key": None}
        if splitter_args is None:
            splitter_args = {
                "chunk_size": 200,
                "chunk_overlap": 20,
                "length_function": "len",
            }
        if not self._has_api_key():
            raise PermissionError(
                "API key not provided.\nEither initialize your client with an API key or login with your username "
                "and password."
            )
        # create pipeline (via api)
        req_headers = {"x-api-key": self._api_key, "Content-Type": "application/json"}
        # Define the endpoint
        endpoint = "/pipelines/create"
        # Define the data to send to the endpoint
        # FIXME: Add some checking here later.
        data = {
            "pipeline_name": name,  # cannot already exist in db
            "splitter": {
                "type": splitter_type,
                "args": splitter_args,
            },
            "embedder": {
                "type": embedder_type,
                "args": embedder_args,
            },
            "vector_store": {
                "type": vector_store_type,
                "args": vector_store_args,
            },
        }
        # Send a POST request to the endpoint
        endpoint = self.API_URL + endpoint
        response = requests.post(
            endpoint,
            data=json.dumps(data),
            headers=req_headers,
        )

        print(endpoint)
        print(response)

        if response.status_code == 200:
            # create and return pipline
            return Pipeline(name, self._api_key)

    def get_pipeline(self, name):
        if not self._has_api_key():
            raise PermissionError(
                "API key not provided.\nEither initialize your client with an API key or login with your username "
                "and password."
            )

        return Pipeline(name, self._api_key)
