import json
from urllib import response
import boto3
import urllib3
from TokenDB import saveAccessToken, getAccessToken
from FuelFinderConnector import getFuelFinderOAuthAccessToken, getFuelPriceData


# HTTP
secrets = boto3.client("secretsmanager")
http = urllib3.PoolManager()

# DB
ttlInSeconds = 1800
dynamodb = boto3.resource("dynamodb")


def getOAuthSecretsForFuelFinderApi() -> dict[str, str]:
    response = secrets.get_secret_value(
        SecretId="govUKfuelFinderOAuthSecret"
    )

    return json.loads(response["SecretString"])



def getBearerToken(accessToken: dict[str,str]) -> str:  
    return accessToken["data"]["access_token"]


def retrieveOrSaveBearerToken() -> str:
    accessToken = getAccessToken(dynamodb)
    if accessToken is not None:
        return accessToken
    else:
        secret = getOAuthSecretsForFuelFinderApi()
        clientId = secret["client_id"]
        clientSecret = secret["client_secret"]
        fuelFinderOAuthAccessToken: dict[str,str] = getFuelFinderOAuthAccessToken(clientId, clientSecret, http)
        print(fuelFinderOAuthAccessToken)
        fuelFinderBearerToken = getBearerToken(fuelFinderOAuthAccessToken)
        print(f"Retrieved new bearer token: {fuelFinderBearerToken}")
        saveAccessToken(fuelFinderBearerToken, ttlInSeconds, dynamodb)
        return fuelFinderBearerToken

def lambda_handler(event, context):
 
    fuelFinderBearerToken = retrieveOrSaveBearerToken()
    response = getFuelPriceData(fuelFinderBearerToken, http)
    print(response)
