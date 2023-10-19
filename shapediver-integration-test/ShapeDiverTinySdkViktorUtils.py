from viktor.utils import memoize
from viktor import UserError, UserMessage
from ShapeDiverTinySdk import ShapeDiverTinySessionSdk
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


def ShapeDiverTinySessionSdkMemoized(ticket, modelViewUrl, forceNewSession=False):
    """Memoized version of ShapeDiverTinySessionSdk
    
    Use this instead of ShapeDiverTinySessionSdk to prevent a new ShapeDiver session
    being created for every computation or export. 
    """

    if forceNewSession: 
        sdk = ShapeDiverTinySessionSdk(ticket = ticket, modelViewUrl = modelViewUrl, exceptionHandler = exceptionHandler)
    else:
        response = __ShapeDiverSessionInitResponseMemoized(ticket = ticket, modelViewUrl = modelViewUrl)
        sdk = ShapeDiverTinySessionSdk(sessionInitResponse = response, modelViewUrl = modelViewUrl, exceptionHandler = exceptionHandler)
    return sdk

