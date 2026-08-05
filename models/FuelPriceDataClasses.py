from dataclasses import dataclass
from typing import List
from datetime import datetime
from decimal import Decimal

# params
#id = node_id
#e5price = fuel_prices[fuelType = E5] price
#e10price = fuel_prices[fuelType = E10] price
@dataclass
class FuelPriceDBRecord:
    id: str
    e5Price: Decimal | None
    e10Price: Decimal | None
    b7StandardPrice: Decimal | None
    b7PremiumPrice: Decimal | None
    b10Price: Decimal | None
    hvoPrice: Decimal | None
    createdAt: int
    ttl: int


@dataclass
class FuelPriceHttpResponse:
    fuel_type: str
    price: float
    price_last_updated: str | None
    price_change_effective_timestamp: str | None


@dataclass
class FuelPriceStationHttpResponse:
    node_id: str
    public_phone_number: str | None
    trading_name: str | None
    fuel_prices: List[FuelPriceHttpResponse]


def convertFuelPriceHttpResponseToDBRecord(fuelPriceStation: FuelPriceStationHttpResponse, createdAt: int, ttl: int) -> FuelPriceDBRecord:
    # Recommend against this normally, but isolated, this isnt so bad
    e5Price = None
    e10Price = None
    b7StandardPrice = None
    b7PremiumPrice = None
    b10Price = None
    hvoPrice = None

    for fuelPrice in fuelPriceStation.fuel_prices:
        if fuelPrice.fuel_type == "E5":
            e5Price = Decimal(str(fuelPrice.price))
        elif fuelPrice.fuel_type == "E10":
            e10Price = Decimal(str(fuelPrice.price))
        elif fuelPrice.fuel_type == "B7_STANDARD":
            b7StandardPrice = Decimal(str(fuelPrice.price))
        elif fuelPrice.fuel_type == "B7_PREMIUM":
            b7PremiumPrice = Decimal(str(fuelPrice.price))
        elif fuelPrice.fuel_type == "B10":
            b10Price = Decimal(str(fuelPrice.price))
        elif fuelPrice.fuel_type == "HVO":
            hvoPrice = Decimal(str(fuelPrice.price))

    return FuelPriceDBRecord(
        id=fuelPriceStation.node_id,
        e5Price=e5Price,
        e10Price=e10Price,
        b7StandardPrice=b7StandardPrice,
        b7PremiumPrice=b7PremiumPrice,
        b10Price=b10Price,
        hvoPrice=hvoPrice,
        createdAt=createdAt,
        ttl=ttl
    )