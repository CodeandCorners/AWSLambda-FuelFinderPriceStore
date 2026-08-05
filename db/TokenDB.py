from datetime import datetime

def saveAccessToken(
    bearer_token: str,
    expires_in: int,
    dynamoDb
) -> None:
    table = dynamoDb.Table("api-tokens")
    expires_at = int(datetime.now().timestamp()) + expires_in

    table.put_item(
        Item={
            "id": "fuel-finder-access-token",
            "bearer_token": bearer_token,
            "insertedAt": str(int(datetime.now().timestamp())),
            "ttl": expires_at
        }
    )
def getAccessToken(dynamoDb) -> str | None:
    table = dynamoDb.Table("api-tokens")
    response = table.get_item(
        Key={
            "id": "fuel-finder-access-token"
        }
    )
    if "Item" not in response:
        return None

    item = response["Item"]

    return item["bearer_token"]
