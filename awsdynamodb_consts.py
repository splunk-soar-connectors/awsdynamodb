# Define your constants here

AWS_DYNAMODB_VALIDATE_INTEGER_MESSAGE = "Please provide a valid integer value in the {key} parameter"
AWS_DYNAMODB_JSON_REGION = "region"
AWS_DYNAMODB_JSON_ACCESS_KEY = "access_key"
AWS_DYNAMODB_JSON_SECRET_KEY = "secret_key"
AWS_DYNAMODB_REGIONS = {
    "US East (Ohio)": "us-east-2",
    "US East (N. Virginia)": "us-east-1",
    "US West (N. California)": "us-west-1",
    "US West (Oregon)": "us-west-2",
    "Asia Pacific (Hong Kong)": "ap-east-1",
    "Canada (Central)": "ca-central-1",
    "Asia Pacific (Mumbai)": "ap-south-1",
    "Asia Pacific (Osaka-Local)": "ap-northeast-3",
    "Asia Pacific (Seoul)": "ap-northeast-2",
    "Asia Pacific (Singapore)": "ap-southeast-1",
    "Asia Pacific (Sydney)": "ap-southeast-2",
    "Asia Pacific (Tokyo)": "ap-northeast-1",
    "China (Beijing)": "cn-north-1",
    "China (Ningxia)": "cn-northwest-1",
    "EU (Frankfurt)": "eu-central-1",
    "EU (Stockholm)": "eu-north-1",
    "EU (Ireland)": "eu-west-1",
    "EU (London)": "eu-west-2",
    "EU (Paris)": "eu-west-3",
    "Middle East (Bahrain)": "me-south-1",
    "AWS GovCloud (US-East)": "us-gov-east-1",
    "AWS GovCloud (US-West)": "us-gov-west-1",
    "South America (São Paulo)": "sa-east-1"
}
AWS_DYNAMODB_DATATYPES = {
    "string": "S",
    "number": "N",
    "binary": "B"
}
AWS_DYNAMODB_KEYTYPE = {
    "sort": "RANGE",
    "partition": 'HASH'
}
EC2_ROLE_CREDENTIALS_FAILURE_MSG = "Failed to get EC2 role credentials"
AWS_DYNAMODB_BAD_ASSET_CONFIG_MSG = "Please provide access keys or select assume role check box in asset configuration"
