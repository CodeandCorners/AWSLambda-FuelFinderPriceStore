import json
import urllib3

def getFuelFinderOAuthAccessToken(clientId: str, clientSecret: str, http: urllib3.PoolManager) -> dict[str,str]:
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

    return json.loads(accessTokenResponse.data.decode("utf-8"))



def getFuelPriceData(bearerToken: str, http: urllib3.PoolManager) -> dict[str, str]:
    fuelPriceResponse = http.request(
        "GET",
        "https://www.fuel-finder.service.gov.uk/api/v1/pfs/fuel-prices?batch-number=99",
        headers={
            "Authorization": f"Bearer {bearerToken}"
        }
    )
    if fuelPriceResponse.status != 200:
        raise Exception(
            f"Fuel price request failed: {fuelPriceResponse.status}"
        )

    return json.loads(fuelPriceResponse.data.decode("utf-8"))
