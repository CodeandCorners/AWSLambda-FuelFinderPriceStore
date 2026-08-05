import json
from models.FuelAuthDataClasses import BearerTokenResponse
import urllib3
from models.FuelPriceDataClasses import FuelPriceStationHttpResponse, FuelPriceHttpResponse
from typing import List


# Example response from API, no idea of optionality
# https://www.developer.fuel-finder.service.gov.uk/fuel-finder/api-guide
# [
#   {
#     "node_id": "0028acef5f3afc41c7e7d56fb285a940dfb64d6fea01cb4accd79c148321112d",
#     "public_phone_number": null,
#     "trading_name": "Alex Fuel Station",
#     "fuel_prices": [
#       {
#         "fuel_type": "E5",
#         "price": 159.9,
#         "price_last_updated": "2026-02-17T16:03:04.938Z",
#         "price_change_effective_timestamp": "2026-02-17T16:00:00.000Z"
#       },
#       {
#         "fuel_type": "E10",
#         "price": 132.9,
#         "price_last_updated": "2026-02-17T16:03:04.938Z",
#         "price_change_effective_timestamp": "2026-02-17T16:00:00.000Z"
#       },
#       {
#         "fuel_type": "B7_STANDARD",
#         "price": 141.9,
#         "price_last_updated": "2026-02-17T16:03:04.938Z",
#         "price_change_effective_timestamp": "2026-02-17T16:00:00.000Z"
#       }
#     ]
#   }]
def getFuelPriceData(bearerToken: BearerTokenResponse, http: urllib3.PoolManager, batchNumber: int) -> List[FuelPriceStationHttpResponse]:
    fuelPriceResponse = http.request(
        "GET",
        f"https://www.fuel-finder.service.gov.uk/api/v1/pfs/fuel-prices?batch-number={batchNumber}",
        headers={
            "Authorization": f"Bearer {bearerToken.bearerToken}"
        }
    )
    if (fuelPriceResponse.status == 404):
        print(f"Fuel price request returned 404, Assumed no more data available for batch number {batchNumber}")
        return []
    elif (fuelPriceResponse.status != 200):
        raise Exception(
            f"Fuel price request failed: {fuelPriceResponse.status}"
        )
    else:
        print(f"Fuel price request returned {fuelPriceResponse.status}, continuing to process data for batch number {batchNumber}")

        jsonResponse = json.loads(fuelPriceResponse.data.decode("utf-8"))
        stations = [
            FuelPriceStationHttpResponse(
            node_id=station["node_id"],
            public_phone_number=station["public_phone_number"],
            trading_name=station["trading_name"],
            fuel_prices=[
                FuelPriceHttpResponse(**price)
            for price in station["fuel_prices"]
            ],
        )
        for station in jsonResponse
    ]   
        print(f"Retrieved {len(stations)} stations for batch number {batchNumber}")

        return stations
