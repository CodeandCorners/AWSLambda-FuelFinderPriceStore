## What
Lambda to update fuel prices from gov uk API, hypothetically once a day, ttl set to EOD for records

API Response models from fuel finder last checked 5th August 2026

## How to
- create one login dev account
- setup application for fuel finder api
- grab client id and secret
- setup AWS secret "govUKfuelFinderOAuthSecret"
{
  "client_secret": "the secret from gov uk dev portal",
  "client_id": "the client id from uk dev portal"
}
- set up lambda in AWS
- create inline policy to point lamda at secret (get secret ARN to use in policy) something like this, but not exactly
```
{
	"Version": "2012-10-17",
	"Statement": [
		{
			"Sid": "ReadFuelFinderSecret",
			"Effect": "Allow",
			"Action": "secretsmanager:GetSecretValue",
			"Resource": "ARN OF SECRET HERE"
		}
	]
}
```
- create dynamoDb table, called "api-tokens"
- turn on TTL, for field "ttl"
- Add inline policy on lambda, just something like this but not exactly
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "FuelFinderTokenCache",
            "Effect": "Allow",
            "Action": [
                "dynamodb:GetItem",
                "dynamodb:PutItem"
            ],
            "Resource": "ARN of TABLE HERE"
        }
    ]
}
```
- create dynamoDb table, called "fuel-prices"
- turn on TTL, for field "ttl"
- partionId on "id"
- Add inline policy on lambda, just something like this but not exactly
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "FuelFinderTokenCache",
            "Effect": "Allow",
            "Action": [
                "dynamodb:GetItem",
                "dynamodb:PutItem",
                "dynamodb:BatchWriteItem"
            ],
            "Resource": "ARN of TABLE HERE"
        }
    ]
}
```
- set timeout in AWS

## Key config
- tokenTTLInSeconds = 1800 # set to 30 mins, token expires in 60, safeguard
- maxBatchNumberForFuelPricesApi = 99 # currently < 10k petrol stations in UK, Rough GOV uk documentation declares 500 per batch? 


## Notes
- Make sure all AWS services are in same zone (i.e. london etc)
- Fuel Price Data TTL set to EOD
- Dynamo DB will overwrite records with same primary key (id) when batch writing