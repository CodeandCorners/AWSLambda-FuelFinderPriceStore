## Lambda to update fuel prices

## How to
- create one login dev account
- setup application for fuel finder api
- grab client id and secret
- setup AWS secret
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