import json
import os
from ShapeDiverTinySdk import ShapeDiverTinySessionSdk

def createParametrization(ticket, modelViewUrl):

    sdk = ShapeDiverTinySessionSdk(ticket = ticket, modelViewUrl = modelViewUrl)
    parameters = [item for item in sdk.response.parameters() if not item['hidden']]
    parameters.sort(key = lambda p: p['order'])
    counter = 0

    for param in parameters:
        ui_name = param['displayname'] if hasattr(param, 'displayname') and len(param['displayname']) > 0 else param['name']
        name = f"ShapeDiverParams.{param['id']}"
        varname = f'param{counter}'
        counter += 1

        if param['type'] == 'Float':
            variant = 'slider' if param['visualization'] == 'slider' else 'standard'
            step = round(pow(0.1, param['decimalplaces']), param['decimalplaces'])
            print(f"{varname} = NumberField('{ui_name}', name='{name}', default={param['defval']}, min={param['min']}, max={param['max']}, num_decimals={param['decimalplaces']}, step={step}, variant='{variant}')")
        elif param['type'] == 'Int':
            variant = 'slider' if param['visualization'] == 'slider' else 'standard'
            print(f"{varname} = NumberField('{ui_name}', name='{name}', default={param['defval']}, min={param['min']}, max={param['max']}, num_decimals=0, step=1, variant='{variant}')")
        elif param['type'] == 'Odd' or param['type'] == 'Even':
            variant = 'slider' if param['visualization'] == 'slider' else 'standard'
            print(f"{varname} = NumberField('{ui_name}', name='{name}', default={param['defval']}, min={param['min']}, max={param['max']}, num_decimals=0, step=2, variant='{variant}')")
        elif param['type'] == 'Bool':
            print(f"{varname} = BooleanField('{ui_name}', name='{name}', default={False if param['defval'] == 'false' else True})")
        elif param['type'] == 'StringList':
            options = []
            for item in param['choices']:
                options.append(f"OptionListElement('{len(options)}', '{item}')")
            varnameOptions = f"{varname}Options"
            print(f"{varnameOptions} = [{', '.join(options)}]")
            print(f"{varname} = OptionField('{ui_name}', name='{name}', options={varnameOptions}, default={param['defval']})")
        #elif param['type'] == 'File':
        #see https://docs.viktor.ai/sdk/api/parametrization/#_FileField
        else:
            print(f"Parameter type {param['type']} not implemented yet.")
            print(param)

    sdk.close()

# ShapeDiver ticket and modelViewUrl
ticket = os.getenv("SD_TICKET")
modelViewUrl = os.getenv("SD_MODEL_VIEW_URL")

createParametrization(ticket, modelViewUrl)