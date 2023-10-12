from viktor import ViktorController, File, UserMessage, UserError
from viktor.parametrization import ViktorParametrization, Text, TextField, NumberField, Section, Image
from viktor.views import GeometryView, GeometryResult
from jsonpath_ng import parse
import requests
import json


class Parametrization(ViktorParametrization):
    intro = Section('Overview')
    intro.image = Image(path = 'logomark_gradient_square_512.png', max_width=64)
    intro.text = Text("""
## ShapeDiver sample app
                      
This app uses [ShapeDiver](https://shapediver.com) to run computations of a Grasshopper script running on ShapeDiver, and visualize its geometric output.
                      
The code for this sample app is available on [GitHub](https://github.com/shapediver/ViktorIntegrationTemplate). Feel free to fork and adapt it to your needs.
    """)

    # Input fields

    ## Ticket and modelViewUrl of ShapeDiver model
    model = Section('ShapeDiver Model')
    model.ticket = TextField('ShapeDiver Backend Ticket', description='Paste a backend ticket for your ShapeDiver model', default='8f3e8c87b953e698033335c697ffe750fc71a58caab67c6cb6de2d24d9d469cae8ff481761b66790b5ea539faca89e570d6a18925727423ad4132a24ad6cfe8d5c8c5f676588145805842d98d7ec4d2a77eb6b5a965e3090796489959337164a872ca36e2e0e2efe36a824ba6c01c222a7df751241f94313-d4beefd5882b0bf59e3d1e54b42e8d54')
    model.modelViewUrl = TextField('ShapeDiver Model View URL', description='Paste the modelViewUrl of your ShapeDiver model', default='https://sdr7euc1.eu-central-1.shapediver.com')
    model.note = Text("""
Learn in our [help center](https://help.shapediver.com/doc/enable-backend-access) how to enable backend access for your ShapeDiver model. 

Here you can find the sample ShapeDiver model used by this app: [AR Cube](https://www.shapediver.com/app/m/augmented-reality-cube-shapediver).
    """)

    ## Parameters of ShapeDiver model (to be investigated how these can be defined dynamically, based on the model)
    ## Note: Set the "name" property to "parameters.{IDENTIFIER}" where {IDENTIFIER} is the id, name, or displayname of the ShapeDiver parameter!
    parameters = Section('Model Parameters')
    parameters.cubes = NumberField('Cubes', name='parameters.Cubes', default=10, min=1, max=20, variant='slider')
    parameters.cubeDensity = NumberField('Cube density', name='parameters.Cube density', default=3, min=1, max=5, variant='slider')
    parameters.note = Text("""
Note: These parameters have been defined statically in the code of this app, based on the parameters of the default ShapeDiver model used by this app. 
Fork the app on [GitHub](https://github.com/shapediver/ViktorIntegrationTemplate) to adapt the parameter definitions to your own ShapeDiver model. 
    """)

  
def runShapeDiverCustomization(ticket, modelViewUrl, paramDict):
    """
    Open a session with a ShapeDiver model, include parameter values in request, return result as JSON.
    """
    endpoint = f'{modelViewUrl}/api/v2/ticket/{ticket}'
    jsonBody = json.dumps(paramDict)
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(endpoint, data=jsonBody, headers=headers)
    if response.status_code != 201:
        raise UserError(f'Failed to run computation (HTTP status code {response.status_code}): {response.text}')

    return response.json()

class Controller(ViktorController):
    label = 'ShapeDiver'
    parametrization = Parametrization

    @GeometryView('ShapeDiver Output Geometry', duration_guess=5, update_label='Run ShapeDiver', up_axis='Y')
    def runShapeDiver(self, params, **kwargs):
        
        # Debug output
        # UserMessage.info(str(params))

        # Get model information from section "model" 
        model = params.model

        # Get parameter values from section "parameters"
        parameters = params.parameters

        # run customization of ShapeDiver model
        response = runShapeDiverCustomization(ticket=model.ticket, modelViewUrl=model.modelViewUrl, paramDict=parameters)
        
        # get the first glTF 2.0 url returned
        # Note: Unfortunately jsonpath filters do not seem to work using the libraries I tested (jsonpath-ng, jsonpath-rw).
        # Probably there is an easier way to achieve getting the glTF url. 
        #jsonpath_expr = parse("$.outputs.*.content[?(@.contentType == 'model/gltf-binary')].href")
        jsonpath_expr = parse('$.outputs.*.content[0]')
        matches = list(filter(lambda item: item['contentType'] == 'model/gltf-binary', [match.value for match in jsonpath_expr.find(response)]))
        if len(matches) < 1:
            raise UserError('Computation did not result in at least one glTF 2.0 asset.')
        
        if len(matches) > 1: 
            UserMessage.warning(f'Computation resulted in {matches.count} glTF 2.0 assets, only displaying the first one.')

        glTF_file = File.from_url(matches[0]['href'])

        return GeometryResult(geometry=glTF_file)
