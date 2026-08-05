import json

from models.FuelAuthDataClasses import BearerTokenResponse

# Example from https://www.developer.fuel-finder.service.gov.uk/fuel-finder/apis-ifr/access-token/docs?operationId=generateAccessToken
#{
#   "success": true,
#   "data": {
#     "access_token": "632ab214482946527e7d7e5f522d4019639add5ebd20795b0d5fd8d19b565153",
#     "token_type": "Bearer",
#     "expires_in": 3600,
#     "refresh_token": "7ad38ea6dbcf1123aef61785b0d6a8f3455bb68734080e0befa440c6ca6ee0eb",
#     "refresh_token_expires_in": 172800
#   },
#   "message": "Operation successful"
# }
def getFuelFinderOAuthAccessToken(clientId: str, clientSecret: str, http: urllib3.PoolManager) -> BearerTokenResponse:
    accessTokenResponse = http.request(
        "POST",
        "https://www.fuel-finder.service.gov.uk/api/v1/oauth/generate_access_token",
        body=json.dumps({
            "client_id": clientId,
            "client_secret": clientSecret
        }),
        headers={
            "Content-Type": "application/json"
        }
    )
    if accessTokenResponse.status != 200:
        raise Exception(
            f"Token request failed: {accessTokenResponse.status}"
        )
    jsonResponse = json.loads(accessTokenResponse.data.decode("utf-8"))
    return BearerTokenResponse(jsonResponse["data"]["access_token"])