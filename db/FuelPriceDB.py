from models.FuelPriceDataClasses import FuelPriceDBRecord
from datetime import datetime


def saveFuelPrices(
    fuel_prices: list[FuelPriceDBRecord],
    dynamoDb
) -> None:
    print(f"Saving {len(fuel_prices)} fuel prices to DynamoDB")
    with dynamoDb.Table("fuel-prices").batch_writer() as batch:
        for fuel_price in fuel_prices:
            item = {
                "id": fuel_price.id,
                "insertedAt": fuel_price.createdAt,
                "ttl": fuel_price.ttl
            }

            optional_fields = {
                "e5Price": fuel_price.e5Price,
                "e10Price": fuel_price.e10Price,
                "b7StandardPrice": fuel_price.b7StandardPrice,
                "b7PremiumPrice": fuel_price.b7PremiumPrice,
                "b10Price": fuel_price.b10Price,
                "hvoPrice": fuel_price.hvoPrice,
            }

            item.update({
                key: value
                for key, value in optional_fields.items()
                if value is not None
            })

            batch.put_item(Item=item)

