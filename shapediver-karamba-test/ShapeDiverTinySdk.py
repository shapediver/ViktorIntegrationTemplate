import json
import requests

def flatten_nested_list(nested_list):
    return [item for sublist in nested_list for item in (flatten_nested_list(sublist) if isinstance(sublist, list) else [sublist])]

class ShapeDiverResponse:
    def __init__(self, response):
        if isinstance(response, str):
            self.response = json.loads(response)
        else:
            self.response = response

    def parameters(self):
        return [value for (key, value) in self.response['parameters'].items()]

    def outputs(self):
        return [value for (key, value) in self.response['outputs'].items()]
       
    def exports(self):
        return [value for (key, value) in self.response['exports'].items()]
    
    def outputContentItems(self):
        return flatten_nested_list([outputs['content'] for outputs in self.outputs()])

    def outputContentItemsGltf2(self):
        return [item for item in self.outputContentItems() if item['contentType'] == 'model/gltf-binary']

    def sessionId(self):
        return self.response['sessionId']
    
class ShapeDiverTinySessionSdk:
    def __init__(self, ticket, modelViewUrl, paramDict = {}):
        """
        Open a session with a ShapeDiver model, optionally include parameter values in request
        """
        self.modelViewUrl = modelViewUrl
        endpoint = f'{modelViewUrl}/api/v2/ticket/{ticket}'
        jsonBody = paramDict if isinstance(paramDict, str) else json.dumps(paramDict)
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.post(endpoint, data=jsonBody, headers=headers)
        if response.status_code != 201:
            raise Exception(f'Failed to run computation (HTTP status code {response.status_code}): {response.text}')

        self.response = ShapeDiverResponse(response.json())

    def close(self):
        """
        Close the session
        """
        endpoint = f'{self.modelViewUrl}/api/v2/session/{self.response.sessionId()}/close'
        response = requests.post(endpoint);
        if response.status_code != 200:
            raise Exception(f'Failed to close session (HTTP status code {response.status_code}): {response.text}')

    