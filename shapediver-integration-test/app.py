from viktor import ViktorController, File, UserMessage, UserError
from viktor.parametrization import ViktorParametrization, Text, TextField, NumberField, Section, Image, ColorField, Color, OptionListElement, OptionField, FileField
from viktor.views import GeometryView, GeometryResult
from ShapeDiverTinySdkViktorUtils import ShapeDiverTinySessionSdkMemoized

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
    ## Note: Set the "name" property to "ShapeDiverParams.{IDENTIFIER}" where {IDENTIFIER} is the id, name, or displayname of the ShapeDiver parameter!
    parameters = Section('Model Parameters')
    parameters.param0 = FileField('Image', name='ShapeDiverParams.9876f55e-2e72-4446-852c-0b3f45f5bcc9', max_size=10485760)
    #parameters.param2 = FileField('Mesh', name='ShapeDiverParams.9bcbbe0d-deff-460c-9658-12b1bd1a4718', max_size=10485760)
    parameters.param3 = NumberField('Cubes', name='ShapeDiverParams.b719ebef-68f7-4c8e-b3b4-0e21b6ffcf4c', default=10, min=1, max=20, num_decimals=0, step=1, variant='slider')
    parameters.param4 = NumberField('Faces per cube', name='ShapeDiverParams.fa076989-c83c-4988-b8b1-473101f16d43', default=2, min=1, max=5, num_decimals=0, step=1, variant='slider')
    parameters.param5 = NumberField('Cube density', name='ShapeDiverParams.87266a9f-04e9-4d0e-bd5f-637243f62070', default=3, min=1, max=5, num_decimals=0, step=1, variant='slider')
    parameters.param6 = NumberField('Field of view', name='ShapeDiverParams.b2804605-f0c4-48de-bca6-ec33b444e24d', default=15.0, min=0, max=90, num_decimals=1, step=0.1, variant='slider')
    parameters.param7 = TextField('Position', name='ShapeDiverParams.4b542891-5f7e-4369-a86b-6182d8ff2204', default='')
    _param8Options = [OptionListElement('0', 'Front'), OptionListElement('1', 'Right'), OptionListElement('2', 'Back'), OptionListElement('3', 'Left'), OptionListElement('4', 'Top'), OptionListElement('5', 'Corner 1'), OptionListElement('6', 'Corner 2'), OptionListElement('7', 'Corner 3'), OptionListElement('8', 'Corner 4')]
    parameters.param8 = OptionField('List', name='ShapeDiverParams.25dcb9a1-26b3-419f-ae16-759256211756', options=_param8Options, default='5')
    parameters.param9 = ColorField('Color', name='ShapeDiverParams.57840b0b-bfa5-4d09-b309-60502c829fd1', default=Color(255,255,255))

    parameters.note = Text("""
Note: These parameters have been defined statically in the code of this app, based on the parameters of the default ShapeDiver model used by this app. 
Fork the app on [GitHub](https://github.com/shapediver/ViktorIntegrationTemplate) to adapt the parameter definitions to your own ShapeDiver model. 
    """)

class Controller(ViktorController):
    label = 'ShapeDiver'
    parametrization = Parametrization

    @GeometryView('ShapeDiver Output Geometry', duration_guess=3, update_label='Run ShapeDiver', up_axis='Y')
    def runShapeDiver(self, params, **kwargs):
        
        # Debug output
        #UserMessage.info(str(params))

        # Get model information from section "model" 
        model = params.model

        # Get parameter values from section "ShapeDiverParams"
        parameters = params.ShapeDiverParams

        # Initialize a session with the model (memoized)
        shapeDiverSessionSdk = ShapeDiverTinySessionSdkMemoized(model.ticket, model.modelViewUrl, forceNewSession = True)

        # compute outputs of ShapeDiver model, get resulting glTF 2 assets
        contentItemsGltf2 = shapeDiverSessionSdk.output(paramDict = parameters).outputContentItemsGltf2()
        
        if len(contentItemsGltf2) < 1:
            raise UserError('Computation did not result in at least one glTF 2.0 asset.')
        
        if len(contentItemsGltf2) > 1: 
            UserMessage.warning(f'Computation resulted in {contentItemsGltf2.count} glTF 2.0 assets, only displaying the first one.')

        glTF_file = File.from_url(contentItemsGltf2[0]['href'])

        return GeometryResult(geometry=glTF_file)
