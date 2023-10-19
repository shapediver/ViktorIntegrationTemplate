from viktor.utils import memoize
from viktor import UserError, UserMessage
from ShapeDiverTinySdk import ShapeDiverTinySessionSdk, RgbToShapeDiverColor
import json

def exceptionHandler(e):
    """VIKTOR-specific exception handler to use for ShapeDiverTinySessionSdk
    
    Adapt this if you want to handle exceptions differently.
    """

    message = e.args[0]
    UserMessage.warning(message)
    raise UserError(message)

@memoize
def __ShapeDiverSessionInitResponseMemoized(ticket, modelViewUrl):
    """Adds support for memoizing ShapeDiver sessions

    see https://docs.viktor.ai/sdk/api/utils/#_memoize
    """

    sdk = ShapeDiverTinySessionSdk(ticket = ticket, modelViewUrl = modelViewUrl, exceptionHandler = exceptionHandler)
    return json.dumps(sdk.response.response)

def parameterMapper(*, paramDict, sdk):
    """Map VIKTOR parameter values to ShapeDiver
    
    This is used to map special value types like Color or File.
    """

    paramDictSd = {}
    paramIds = [key for (key, value) in paramDict.items()]
    for paramId in paramIds:
        if paramId in sdk.response.response['parameters']:
            paramDef = sdk.response.response['parameters'][paramId]
            if paramDef['type'] == 'Color':
                color = paramDict[paramId]
                paramDictSd[paramId] = RgbToShapeDiverColor(color.r, color.g, color.b)
            else:
                paramDictSd[paramId] = paramDict[paramId]
        else:
            paramDictSd[paramId] = paramDict[paramId]

    return paramDictSd

def ShapeDiverTinySessionSdkMemoized(ticket, modelViewUrl, forceNewSession=False):
    """Memoized version of ShapeDiverTinySessionSdk
    
    Use this instead of ShapeDiverTinySessionSdk to prevent a new ShapeDiver session
    being created for every computation or export. 
    """

    if forceNewSession: 
        sdk = ShapeDiverTinySessionSdk(ticket = ticket, modelViewUrl = modelViewUrl, 
            exceptionHandler = exceptionHandler, parameterMapper = parameterMapper)
    else:
        response = __ShapeDiverSessionInitResponseMemoized(ticket = ticket, modelViewUrl = modelViewUrl)
        sdk = ShapeDiverTinySessionSdk(sessionInitResponse = response, modelViewUrl = modelViewUrl, 
            exceptionHandler = exceptionHandler, parameterMapper = parameterMapper)
    return sdk

