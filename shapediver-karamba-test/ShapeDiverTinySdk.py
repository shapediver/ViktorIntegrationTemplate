import json
import requests

def flatten_nested_list(nested_list):
    return [item for sublist in nested_list for item in (flatten_nested_list(sublist) if isinstance(sublist, list) else [sublist])]

class ShapeDiverResponse:
    """Wrapper for response objects from ShapeDiver Geometry Backend systems

    See API documentation: https://sdr7euc1.eu-central-1.shapediver.com/api/v2/docs/
    """

    def __init__(self, response):
        if isinstance(response, str):
            self.response = json.loads(response)
        else:
            self.response = response

    def parameters(self):
        """Parameter definitions

        Look for ResponseParameter in the API documentation.
        """

        return [value for (key, value) in self.response['parameters'].items()]

    def outputs(self):
        """Output definitions and results

        Look for ResponseOutput in the API documentation.
        """

        return [value for (key, value) in self.response['outputs'].items()]
       
    def outputContentItems(self):
        """Content resulting from outputs

        Look for ResponseOutputContent in the API documentation.
        """

        return flatten_nested_list([outputs['content'] for outputs in self.outputs()])

    def outputContentItemsGltf2(self):
        """glTF 2 content resulting from outputs

        Look for ResponseOutputContent in the API documentation.
        """

        return [item for item in self.outputContentItems() if item['contentType'] == 'model/gltf-binary']

    def exports(self):
        """Export definitions and results

        Look for ResponseExport in the API documentation.
        """

        return [value for (key, value) in self.response['exports'].items()]
    
    def exportContentItems(self):
        """Content resulting from exports

        Look for ResponseExportContent in the API documentation.
        """

        return flatten_nested_list([exports['content'] for exports in self.exports()])
    
    def sessionId(self):
        """Id of the session"""

        return self.response['sessionId']
    
class ShapeDiverTinySessionSdk:
    """A minimal Python SDK to handle sessions with ShapeDiver Geometry Backend Systems.
    
    """

    def __init__(self, modelViewUrl, ticket=None, sessionInitResponse=None, paramDict = {}):
        """Open a session with a ShapeDiver model
        
        Parameter values can optionally be included in the session init request.
        API documentation: https://sdr7euc1.eu-central-1.shapediver.com/api/v2/docs/#/session/post_api_v2_ticket__ticketId_
        """

        self.modelViewUrl = modelViewUrl
      
        if sessionInitResponse is not None:
            self.response = ShapeDiverResponse(sessionInitResponse)
      
        elif ticket is not None:
            endpoint = f'{self.modelViewUrl}/api/v2/ticket/{ticket}'
            jsonBody = paramDict if isinstance(paramDict, str) else json.dumps(paramDict)
            headers = {
                'Content-Type': 'application/json'
            }
            response = requests.post(endpoint, data=jsonBody, headers=headers)
            if response.status_code != 201:
                raise Exception(f'Failed to run computation (HTTP status code {response.status_code}): {response.text}')

            # TODO: handle rate-limiting and delay

            """Parsed response of the session init request"""
            self.response = ShapeDiverResponse(response.json())
        else:
            raise Exception('Expected (ticket and modelViewUrl) or (sessionInitResponse and modelViewUrl) to be provided')

    def close(self):
        """Close the session
        
        API documentation: https://sdr7euc1.eu-central-1.shapediver.com/api/v2/docs/#/session/post_api_v2_session__sessionId__close
        """

        endpoint = f'{self.modelViewUrl}/api/v2/session/{self.response.sessionId()}/close'
        response = requests.post(endpoint);
        if response.status_code != 200:
            raise Exception(f'Failed to close session (HTTP status code {response.status_code}): {response.text}')

    def output(self, paramDict = {}):
        """Request the computation of all outputs

        API documentation: https://sdr7euc1.eu-central-1.shapediver.com/api/v2/docs/#/output/put_api_v2_session__sessionId__output
        """

        endpoint = f'{self.modelViewUrl}/api/v2/session/{self.response.sessionId()}/output'
        jsonBody = json.dumps(paramDict)
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.put(endpoint, data=jsonBody, headers=headers)
        if response.status_code != 200:
            raise Exception(f'Failed to compute outputs (HTTP status code {response.status_code}): {response.text}')

        # TODO: handle rate-limiting and delay

        return ShapeDiverResponse(response.json())

    def export(self, exportId, paramDict = {}):
        """Request an export

        API documentation: https://sdr7euc1.eu-central-1.shapediver.com/api/v2/docs/#/export/put_api_v2_session__sessionId__export
        """

        endpoint = f'{self.modelViewUrl}/api/v2/session/{self.response.sessionId()}/export'
        body = {'exports': [exportId], 'parameters': paramDict}
        jsonBody = json.dumps(body)
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.put(endpoint, data=jsonBody, headers=headers)
        if response.status_code != 200:
            raise Exception(f'Failed to run export (HTTP status code {response.status_code}): {response.text}')

        # TODO: handle rate-limiting and delay

        return ShapeDiverResponse(response.json())
    