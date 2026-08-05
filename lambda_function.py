from datetime import datetime, time
import json
from typing import List
from urllib import response
from models.FuelPriceDataClasses import FuelPriceDBRecord, FuelPriceStationHttpResponse, convertFuelPriceHttpResponseToDBRecord
from models.FuelAuthDataClasses import BearerTokenResponse
import boto3
import urllib3
from db.TokenDB import saveAccessToken, getAccessToken
from db.FuelPriceDB import saveFuelPrices
from connectors.FuelFinderOAuthConnector import getFuelFinderOAuthAccessToken
from connectors.FuelFinderPricesConnector import getFuelPriceData


# HTTP
maxBatchNumberForFuelPricesApi = 99
secrets = boto3.client("secretsmanager")
http = urllib3.PoolManager()

# DB
tokenTTLInSeconds = 1800
maxBatchNumberForFuelPricesApi = 99
dynamodb = boto3.resource("dynamodb")


def getOAuthSecretsForFuelFinderApi() -> dict[str, str]:
    response = secrets.get_secret_value(
        SecretId="govUKfuelFinderOAuthSecret"
    )

    return json.loads(response["SecretString"])


def retrieveOrSaveBearerToken() -> BearerTokenResponse:
    accessToken = getAccessToken(dynamodb)
    if accessToken is not None:
        print("Access token found in DB, no API call needed")
        return BearerTokenResponse(accessToken)
    else:
        print("No access token found in DB, making API call")
        secret = getOAuthSecretsForFuelFinderApi()
        clientId = secret["client_id"]
        clientSecret = secret["client_secret"]
        fuelFinderBearerToken: BearerTokenResponse = getFuelFinderOAuthAccessToken(clientId, clientSecret, http)
        
        saveAccessToken(fuelFinderBearerToken.bearerToken, tokenTTLInSeconds, dynamodb)
        return fuelFinderBearerToken

def fuelPriceGetAndInsert(bearerToken: BearerTokenResponse, batchNumber: int, createdAt: int, ttl: int) -> bool:
    fuelPriceData: List[FuelPriceStationHttpResponse] = getFuelPriceData(bearerToken, http, batchNumber)

    if len(fuelPriceData) > 0:
        convertedData: List[FuelPriceDBRecord] = [
            convertFuelPriceHttpResponseToDBRecord(station, createdAt, ttl)
            for station in fuelPriceData
        ]
        saveFuelPrices(convertedData, dynamodb)
    return len(fuelPriceData) > 0

def fuelPriceInsertOrchestrator(bearerToken: BearerTokenResponse):
    now = datetime.now()
    dateTimeNow: int = int(now.timestamp())
    ttlOfDataRetrieved: int = int(datetime.combine(now.date(), time(23, 59, 59)).timestamp())
 
    batchNumber = 1
    while batchNumber <= maxBatchNumberForFuelPricesApi:
        print(f"Processing batch number {batchNumber}")
        hasDataInBatch: bool = fuelPriceGetAndInsert(bearerToken, batchNumber, dateTimeNow, ttlOfDataRetrieved)
        if not hasDataInBatch:
            print(f"No data returned for batch number {batchNumber}, stopping processing")
            break
        batchNumber += 1

def lambda_handler(event, context):
 
    fuelFinderBearerToken = retrieveOrSaveBearerToken()
    fuelPriceInsertOrchestrator(fuelFinderBearerToken)
    return "Updated fuel-prices in DynamoDB"

