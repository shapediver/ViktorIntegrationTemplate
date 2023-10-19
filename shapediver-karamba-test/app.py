from viktor import ViktorController, File, UserMessage, UserError
from viktor.parametrization import ViktorParametrization, Text, TextField, NumberField, Section, Image
from viktor.views import GeometryView, GeometryResult, ImageView, ImageResult, PDFView, PDFResult
from ShapeDiverTinySdkViktorUtils import ShapeDiverTinySessionSdkMemoized
import os

# ShapeDiver ticket and modelViewUrl
ticket = os.getenv("SD_TICKET")
modelViewUrl = os.getenv("SD_MODEL_VIEW_URL")

class Parametrization(ViktorParametrization):
    intro = Section('Overview')
    intro.image = Image(path = 'logomark_gradient_square_512.png', max_width=64)
    intro.text = Text("""
## ShapeDiver sample app using Karamba3D
                      
This app uses [ShapeDiver](https://shapediver.com) to run computations of a Grasshopper script running on ShapeDiver, and visualize its geometric output.
                      
The code for this sample app is available on [GitHub](https://github.com/shapediver/ViktorIntegrationTemplate). Feel free to fork and adapt it to your needs.
    """)

    # Input fields
    parameters = Section('Model Parameters')
    parameters.trussLength = NumberField('Truss length [m]', name='ShapeDiverParams.06353841-58a1-41e8-966c-6ba817cce062', default=10, min=5, max=50, num_decimals=0, step=1, variant='slider' )
    parameters.trussHeight = NumberField('Truss height [m]', name='ShapeDiverParams.6e1ea058-a76b-48aa-97df-666f93e474ba', default=1.2, min=0, max=5, num_decimals=1, step=0.1, variant='slider' )
    parameters.pointLoad = NumberField('Point Load [kN]', name='ShapeDiverParams.5cd39465-987a-423e-b6d8-5e35a4e61f36', default=50, min=0, max=200, num_decimals=0, step=1, variant='slider' )
    parameters.positionPointLoad = NumberField('Position - Point Load', name='ShapeDiverParams.d43d900f-e6ec-4e00-9959-76f111124089', default=0.5, min=0, max=1, num_decimals=2, step=0.01, variant='slider' )

class Controller(ViktorController):
    label = 'ShapeDiver'
    parametrization = Parametrization
    
  
    @GeometryView('ShapeDiver Output Geometry', duration_guess=1, update_label='Run ShapeDiver Computation', up_axis='Y')
    def runShapeDiver(self, params, **kwargs):
        
        # Debug output
        # UserMessage.info(str(params))

        # Get parameter values from section "parameters"
        parameters = params.ShapeDiverParams

        # Initialize a session with the model (memoized)
        shapeDiverSessionSdk = ShapeDiverTinySessionSdkMemoized(ticket, modelViewUrl)

        # compute outputs of ShapeDiver model, get resulting glTF 2 assets
        contentItemsGltf2 = shapeDiverSessionSdk.output(parameters).outputContentItemsGltf2()
        
        if len(contentItemsGltf2) < 1:
            raise UserError('Computation did not result in at least one glTF 2.0 asset.')
        
        if len(contentItemsGltf2) > 1: 
            UserMessage.warning(f'Computation resulted in {contentItemsGltf2.count} glTF 2.0 assets, only displaying the first one.')

        glTF_file = File.from_url(contentItemsGltf2[0]['href'])

        return GeometryResult(geometry=glTF_file)

    @ImageView("Image", duration_guess=1, update_label='Run ShapeDiver Image Export')
    def runShapeDiverImageExport(self, params, **kwargs):

        # Debug output
        # UserMessage.info(str(params))

        # Get parameter values from section "parameters"
        parameters = params.ShapeDiverParams

        # Initialize a session with the model (memoized)
        shapeDiverSessionSdk = ShapeDiverTinySessionSdkMemoized(ticket, modelViewUrl)

        # get id of image export
        imageExportId = [exp['id'] for exp in shapeDiverSessionSdk.response.exports() if exp['displayname'] == 'Download Png'][0]

        # run the export
        exportItems = shapeDiverSessionSdk.export(imageExportId, parameters).exportContentItems()
            
        if len(exportItems) < 1:
            raise UserError('Export did not result in an image.')
        
        if len(exportItems) > 1: 
            UserMessage.warning(f'Export resulted in {exportItems.count} images, only displaying the first one.')

        image_file = File.from_url(exportItems[0]['href'])

        return ImageResult(image_file)

    @PDFView("PDF", duration_guess=1, update_label='Run ShapeDiver PDF Export')
    def runShapeDiverPdfExport(self, params, **kwargs):

        # Debug output
        # UserMessage.info(str(params))

        # Get parameter values from section "parameters"
        parameters = params.ShapeDiverParams

        # Initialize a session with the model (memoized)
        shapeDiverSessionSdk = ShapeDiverTinySessionSdkMemoized(ticket, modelViewUrl)

        # get id of image export
        pdfExportId = [exp['id'] for exp in shapeDiverSessionSdk.response.exports() if exp['displayname'] == 'Download Pdf'][0]

        # run the export
        exportItems = shapeDiverSessionSdk.export(pdfExportId, parameters).exportContentItems()
            
        if len(exportItems) < 1:
            raise UserError('Export did not result in a PDF.')
        
        if len(exportItems) > 1: 
            UserMessage.warning(f'Export resulted in {exportItems.count} PDFs, only displaying the first one.')

        pdf_file = File.from_url(exportItems[0]['href'])

        return PDFResult(file=pdf_file)
        