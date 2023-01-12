# File: awsdynamodb_consts.py
#
# Copyright (c) 2023 Splunk Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions
# and limitations under the License.

AWS_DYNAMODB_VALIDATE_INTEGER_MESSAGE = "Please provide a valid integer value in the {key} parameter"
ERROR_MESSAGE_UNAVAILABLE = "Error message unavailable. Please check the asset configuration and|or action parameters"
AWS_DYNAMODB_JSON_REGION = "region"
AWS_DYNAMODB_JSON_ACCESS_KEY = "access_key"
AWS_DYNAMODB_JSON_SECRET_KEY = "secret_key"  # pragma: allowlist secret`
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
EC2_ROLE_CREDENTIALS_FAILURE_MESSAGE = "Failed to get EC2 role credentials"
AWS_DYNAMODB_BAD_ASSET_CONFIG_MESSAGE = "Please provide access keys or select assume role check box in asset configuration"
AWS_DATE_TIME_CONVERSION = "Converting datetime object to string"
AWS_BOTO_CALL = "Making boto call to DynamoDB"
