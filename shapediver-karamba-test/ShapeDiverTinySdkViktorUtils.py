from viktor.utils import memoize
from ShapeDiverTinySdk import ShapeDiverTinySessionSdk
import json

# see https://docs.viktor.ai/sdk/api/utils/#_memoize
@memoize
def __ShapeDiverSessionInitResponseMemoized(ticket, modelViewUrl):
    sdk = ShapeDiverTinySessionSdk(ticket = ticket, modelViewUrl = modelViewUrl)
    return json.dumps(sdk.response.response)

def ShapeDiverTinySessionSdkMemoized(ticket, modelViewUrl):
    response = __ShapeDiverSessionInitResponseMemoized(ticket = ticket, modelViewUrl = modelViewUrl)
    return ShapeDiverTinySessionSdk(sessionInitResponse = response, modelViewUrl = modelViewUrl)


