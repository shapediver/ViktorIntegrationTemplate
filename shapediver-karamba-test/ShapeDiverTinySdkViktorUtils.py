from viktor.utils import memoize
from viktor import UserError, UserMessage
from ShapeDiverTinySdk import ShapeDiverTinySessionSdk
import json

def exceptionHandler(e):
    """VIKTOR-specific exception handler to use for ShapeDiverTinySessionSdk"""
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


def ShapeDiverTinySessionSdkMemoized(ticket, modelViewUrl):
    response = __ShapeDiverSessionInitResponseMemoized(ticket = ticket, modelViewUrl = modelViewUrl)
    sdk = ShapeDiverTinySessionSdk(sessionInitResponse = response, modelViewUrl = modelViewUrl, exceptionHandler = exceptionHandler)
    return sdk

