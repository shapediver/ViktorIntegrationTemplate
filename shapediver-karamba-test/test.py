import json
from ShapeDiverTinySdk import ShapeDiverTinySessionSdk

ticket = "718c311d77a31ceda3f46367a6b9c885883ab054ad37a191096e21974281f2ec52e97eda54eb378d689c1e858889a5ff63a6574459d801f3e9a2a48da62d11eba3c841b8c1d04e8a92b8cc20361cc83600a8e766aaaf0f8a154844e31740c595b31b275c7ce096d3c9adc7b20c08557eae446de69095ed91-c070fb14f2e811b5c2a79fddb9b4f0c8"
modelViewUrl = "https://sddev3.eu-central-1.shapediver.com"

sessionSdk = ShapeDiverTinySessionSdk(ticket, modelViewUrl)

# print(sessionSdk.response.outputContentItemsGltf2())

# print(sessionSdk.response.exports())

imageExportId = [exp['id'] for exp in sessionSdk.response.exports() if exp['displayname'] == 'Download Png'][0]
# print(imageExportId)

exportResponse = sessionSdk.export(imageExportId)
print(exportResponse.exportContentItems()[0]['href'])

sessionSdk.close()