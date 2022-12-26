# File: awsdynamodb_connector.py
#
# Copyright (c) 2022 Splunk Inc.
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


import ast
import json
from datetime import datetime

import phantom.app as phantom
import requests
from boto3 import Session, client
from botocore.config import Config
from dateutil.parser import parse
from phantom.action_result import ActionResult
from phantom.base_connector import BaseConnector

from awsdynamodb_consts import *

# Phantom App imports


class RetVal(tuple):

    def __new__(cls, val1, val2=None):
        return tuple.__new__(RetVal, (val1, val2))


class AwsDynamodbConnector(BaseConnector):

    def __init__(self):

        # Call the BaseConnectors init first
        super(AwsDynamodbConnector, self).__init__()
        self._state = None
        self._client = None
        self._region = None
        self._access_key = None
        self._secret_key = None
        self._session_token = None
        self._proxy = None

    def initialize(self):
        self._state = self.load_state()

        # get the asset config
        config = self.get_config()

        self._region = AWS_DYNAMODB_REGIONS.get(
            config[AWS_DYNAMODB_JSON_REGION])

        self._proxy = {}
        env_vars = config.get('_reserved_environment_variables', {})
        if 'HTTP_PROXY' in env_vars:
            self._proxy['http'] = env_vars['HTTP_PROXY']['value']
        if 'HTTPS_PROXY' in env_vars:
            self._proxy['https'] = env_vars['HTTPS_PROXY']['value']

        if config.get('use_role'):
            credentials = self._handle_get_ec2_role()
            if not credentials:
                return self.set_status(phantom.APP_ERROR, EC2_ROLE_CREDENTIALS_FAILURE_MESSAGE)
            self._access_key = credentials.access_key
            self._secret_key = credentials.secret_key
            self._session_token = credentials.token

            return phantom.APP_SUCCESS

        self._access_key = config.get(AWS_DYNAMODB_JSON_ACCESS_KEY)
        self._secret_key = config.get(AWS_DYNAMODB_JSON_SECRET_KEY)

        if not (self._access_key and self._secret_key):
            return self.set_status(phantom.APP_ERROR, AWS_DYNAMODB_BAD_ASSET_CONFIG_MESSAGE)

        return phantom.APP_SUCCESS

    def finalize(self):
        # Save the state, this data is saved across actions and app upgrades
        self.save_state(self._state)
        return phantom.APP_SUCCESS

    def _validate_integer(self, action_result, parameter, key, allow_zero=False):
        """ This method is to check if the provided input parameter value
        is a non-zero positive integer and returns the integer value of the parameter itself.
        :param action_result: Action result or BaseConnector object
        :param parameter: input parameter
        :return: integer value of the parameter or None in case of failure
        """
        if parameter is not None:
            try:
                if not float(parameter).is_integer():
                    return action_result.set_status(
                        phantom.APP_ERROR, AWS_DYNAMODB_VALIDATE_INTEGER_MESSAGE.format(key=key)), None
                parameter = int(parameter)

            except Exception:
                return action_result.set_status(
                    phantom.APP_ERROR, AWS_DYNAMODB_VALIDATE_INTEGER_MESSAGE.format(key=key)), None

            if parameter < 0:
                return action_result.set_status(
                    phantom.APP_ERROR, "Please provide a valid non-negative integer value in the {} parameter".format(key)), None

            if not allow_zero and parameter == 0:
                return action_result.set_status(
                    phantom.APP_ERROR, "Please provide a positive integer value in the {} parameter".format(key)), None

        return phantom.APP_SUCCESS, parameter

    def _handle_get_ec2_role(self):

        session = Session(region_name=self._region)
        credentials = session.get_credentials()
        return credentials

    def _handle_comma_separated_string(self, comma_str):
        """
        Convert comma separated string into list.

        :param comma_str: comma separated string
        :return : list
        """
        str_to_list = [x.strip() for x in comma_str.split(",") if x]
        return str_to_list

    def _parse_json_for_indexes(self, action_result, key_data, original_resp, index_type, table_partition_key=""):
        """
        Parse values for global and local secondary in

        Args:
            action_result : Action result or BaseConnector object
            key_data : json data from which key values are to be parsed
            original_resp : payload in which key values are to be added
            index_type : type of index key (Local/Global)
            table_partition_key : Partition key provided for the table. Defaults to "".

        Returns:
            _type_: _description_
        """

        attribute_definitions = []

        for data in key_data:
            if not isinstance(data, dict):
                return action_result.set_status(
                    phantom.APP_ERROR,
                    "DICT CHECK Invalid input passed for creating {} secondary index".format(
                        index_type
                    )
                )

                # basic structure for index objects
            index_key_object = {
                "KeySchema": [],
                "Projection": {
                    "ProjectionType": '',
                }
            }

            key_projection = data.get('attribute_projection')
            sort_key_name = data.get('sort_key_name')
            partition_key_name = data.get('partition_key_name')
            sort_key_datatype = data.get('sort_key_datatype')
            partition_key_datatype = data.get('partition_key_datatype')

            if sort_key_datatype:
                sort_key_datatype = AWS_DYNAMODB_DATATYPES.get(
                    sort_key_datatype.lower())

            if partition_key_datatype:
                partition_key_datatype = AWS_DYNAMODB_DATATYPES.get(
                    partition_key_datatype.lower())

            if key_projection:
                # condition to local secondary index
                if index_type == "Local" and sort_key_name and sort_key_datatype:

                    attribute_definitions.append({
                        "AttributeName": sort_key_name,
                        "AttributeType": sort_key_datatype,
                    })
                    index_key_object["IndexName"] = "{}-index".format(
                        sort_key_name)
                    index_key_object["KeySchema"].extend([
                        {
                            "AttributeName": table_partition_key,
                            "KeyType": "HASH",
                        },
                        {
                            "AttributeName": sort_key_name,
                            "KeyType": "RANGE",
                        }
                    ])
                    index_key_object["Projection"] = {
                        "ProjectionType": key_projection
                    }
                    original_resp["LocalSecondaryIndexes"].append(
                        index_key_object)

                # condition for global secondary index
                elif index_type == "Global" and partition_key_name and partition_key_datatype:

                    attribute_definitions.append({
                        "AttributeName": partition_key_name,
                        "AttributeType": partition_key_datatype
                    })
                    index_key_object['KeySchema'].append({
                        'AttributeName': partition_key_name,
                        'KeyType': 'HASH'
                    })
                    if sort_key_name and sort_key_datatype:
                        attribute_definitions.append({
                            "AttributeName": sort_key_name,
                            "AttributeType": sort_key_datatype
                        })
                        index_key_object['KeySchema'].append({
                            'AttributeName': sort_key_name,
                            'KeyType': 'RANGE'
                        })

                    index_key_object["Projection"] = {
                        "ProjectionType": key_projection
                    }
                    index_key_name = "{}-{}-index".format(
                        partition_key_name, sort_key_name) if sort_key_name and partition_key_name else "{}-index".format(partition_key_name)
                    index_key_object['IndexName'] = index_key_name
                    if original_resp['BillingMode'] == "PROVISIONED":
                        index_key_object['ProvisionedThroughput'] = original_resp['ProvisionedThroughput']

                    original_resp["GlobalSecondaryIndexes"].append(
                        index_key_object)
                else:
                    return action_result.set_status(phantom.APP_ERROR, "Invalid input passed for creating {} Secondary Index".format(index_type))

                if key_projection == "INCLUDE":
                    attributes = data.get('non_key_attributes')
                    if len(attributes) > 0:
                        if isinstance(attributes, list) and all(isinstance(x, str) for x in attributes):
                            index_key_object["Projection"]["NonKeyAttributes"] = attributes
                        else:
                            print('Invalid List Attributes passed')
                    else:
                        error_in_index = ""
                        if index_type == 'Local':
                            error_in_index = sort_key_name
                        elif index_type == "Global":
                            error_in_index = partition_key_name
                        return action_result.set_status(
                            phantom.APP_ERROR,
                            "Please enter a value in non_key_attributes field for a {} key  in {} Secondary Index".format(
                                error_in_index,
                                index_type
                            )
                        )

            else:
                return action_result.set_status(phantom.APP_ERROR, "Invalid input passed for creating secondary index")

        original_resp['AttributeDefinitions'].extend(attribute_definitions)
        return phantom.APP_SUCCESS

    def _create_client(self, action_result, param=None):

        boto_config = None
        if self._proxy:
            boto_config = Config(proxies=self._proxy)

        # Try getting and using temporary assume role credentials from parameters
        temp_credentials = dict()
        if param and 'credentials' in param:
            try:
                temp_credentials = ast.literal_eval(param['credentials'])
                self._access_key = temp_credentials.get('AccessKeyId', '')
                self._secret_key = temp_credentials.get('SecretAccessKey', '')
                self._session_token = temp_credentials.get('SessionToken', '')

                self.save_progress(
                    "Using temporary assume role credentials for action")
            except Exception as e:
                return action_result.set_status(phantom.APP_ERROR,
                                                "Failed to get temporary credentials: {0}".format(e))
        try:

            if self._access_key and self._secret_key:
                self.debug_print("Creating boto3 client with API keys")
                self._client = client(
                    'dynamodb',
                    region_name=self._region,
                    aws_access_key_id=self._access_key,
                    aws_secret_access_key=self._secret_key,
                    aws_session_token=self._session_token,
                    config=boto_config
                )

            else:
                self.debug_print("Creating boto3 client without API keys")
                self._client = client(
                    'dynamodb',
                    region_name=self._region,
                    config=boto_config)

        except Exception as e:
            return action_result.set_status(phantom.APP_ERROR, "Could not create boto3 client: {0}".format(e))

        return phantom.APP_SUCCESS

    def _make_boto_call(self, action_result, method, kwargs={}):

        try:
            boto_func = getattr(self._client, method)
        except AttributeError:
            return RetVal(action_result.set_status(phantom.APP_ERROR, "Invalid method: {0}".format(method)), None)

        try:
            resp_json = boto_func(**kwargs)
        except Exception as e:
            return RetVal(action_result.set_status(phantom.APP_ERROR, 'boto3 call to Dynamodb failed', str(e)), None)

        return phantom.APP_SUCCESS, resp_json

    def _paginator(self, action_result, method, kwargs):

        try:
            boto_func = getattr(self._client, "get_paginator")(method)
        except AttributeError:
            return RetVal(action_result.set_status(phantom.APP_ERROR, "Invalid method: {0}".format(method)), None)

        resp_object = boto_func.paginate(**kwargs)

        return phantom.APP_SUCCESS, resp_object

    def _create_table(self, param):  # noqa: C901
        """
        Create a table in the DynamoDB database
        """

        action_result = self.add_action_result(ActionResult(dict(param)))
        if not self._create_client(action_result, param):
            return action_result.get_status()

        # tablename
        table_name = param['table_name']

        # partition key
        partition_key_name = param['partition_key_name']
        partition_key_datatype = param['partition_key_datatype']

        # sort key
        sort_key_name = param.get('sort_key_name')
        sort_key_datatype = param.get('sort_key_datatype')

        # billing mode
        billing_mode = param.get('billing_mode', "PROVISIONED")

        # local secondary index
        local_sec_index = param.get('local_secondary_index')
        global_sec_index = param.get('global_secondary_index')

        sse = param["sse"]
        kms_master_key_id = param.get("kms_master_key_id")

        enable_stream = param.get("enable_stream")
        stream_view_type = param.get("stream_view_type")
        tags = param.get("tags")

        # payload to send
        payload = {
            "TableName": table_name,
            "AttributeDefinitions": [
                {
                    "AttributeName": partition_key_name,
                    "AttributeType": AWS_DYNAMODB_DATATYPES.get(partition_key_datatype.lower())
                }
            ],
            "KeySchema": [
                {
                    "AttributeName": partition_key_name,
                    "KeyType": 'HASH'
                }
            ],
            "BillingMode": billing_mode
        }

        if sort_key_name:
            if sort_key_datatype:
                payload['AttributeDefinitions'].append({
                    "AttributeName": sort_key_name,
                    "AttributeType": AWS_DYNAMODB_DATATYPES.get(sort_key_datatype.lower())
                })
                payload['KeySchema'].append({
                    "AttributeName": sort_key_name,
                    "KeyType": 'RANGE'
                })
            else:
                return action_result.set_status(
                    phantom.APP_ERROR, "Please enter a datatype for sort key")

        if billing_mode == "PROVISIONED":
            # read capacity
            ret_val, read_units = self._validate_integer(
                action_result,
                param.get('read_capacity_units', 5),
                'read capacity units'
            )
            if (phantom.is_fail(ret_val)):
                return action_result.get_status()

            ret_val, write_units = self._validate_integer(
                action_result,
                param.get('write_capacity_units', 5),
                'write capacity units'
            )
            if (phantom.is_fail(ret_val)):
                return action_result.get_status()

            payload['ProvisionedThroughput'] = {
                'ReadCapacityUnits': read_units,
                'WriteCapacityUnits': write_units,
            }

        self.debug_print("Parsing data for local indexes")
        # handle local secondary index
        if local_sec_index:
            payload["LocalSecondaryIndexes"] = list()
            try:
                local_sec_index = json.loads(local_sec_index)
            except Exception as e:
                return action_result.set_status(
                    phantom.APP_ERROR, "Invalid Json data for Local Secondary Index : {}".format(e))

            if isinstance(local_sec_index, dict):
                local_sec_index = [local_sec_index]
            elif not isinstance(local_sec_index, list):
                return action_result.set_status(
                    phantom.APP_ERROR,
                    "Invalid data format for LSI, please enter data in valid format as mentioned in documentation"
                )

            if len(local_sec_index) > 5:
                return action_result.set_status(
                    phantom.APP_ERROR,
                    "Index limit exceeded, can create only 5 local secondary at max. Please enter 5 or less keys data"
                )

            ret_val = self._parse_json_for_indexes(
                action_result,
                local_sec_index,
                payload,
                "Local",
                table_partition_key=partition_key_name
            )

            if (phantom.is_fail(ret_val)):
                return ret_val

        # handle global secondary index
        if global_sec_index:
            payload["GlobalSecondaryIndexes"] = []
            try:
                global_sec_index = json.loads(global_sec_index)
            except Exception as e:
                return action_result.set_status(
                    phantom.APP_ERROR, "Invalid Json data for Global Secondary Index : {}".format(e))

            if len(global_sec_index) > 20:
                return action_result.set_status(
                    phantom.APP_ERROR,
                    "Index limit exceeded, can create only 20 local secondary at max. Please enter 20 or less keys data"
                )

            if isinstance(global_sec_index, dict):
                global_sec_index = [global_sec_index]
            elif not isinstance(global_sec_index, list):
                return action_result.set_status(
                    phantom.APP_ERROR,
                    "Invalid data format for GSI, please enter data in valid format as mentioned in documentation"
                )

            ret_val = self._parse_json_for_indexes(
                action_result,
                global_sec_index,
                payload,
                "Global"
            )
            if (phantom.is_fail(ret_val)):
                return ret_val

        if sse == "True":
            payload["SSESpecification"] = {
                "Enabled": True,
                "SSEType": "KMS"
            }
            if kms_master_key_id:
                payload["SSESpecification"] = {
                    "KMSMasterKeyId": kms_master_key_id
                }
        elif sse == "False":
            payload["SSESpecification"] = {
                "Enabled": False
            }

        if enable_stream:
            payload["StreamSpecification"] = dict()
            if stream_view_type:
                payload["StreamSpecification"]["StreamEnable"] = enable_stream
                payload["StreamSpecification"]["StreamViewType"] = stream_view_type

            else:
                return action_result.set_status(phantom.APP_ERROR, "Please select a stream view type")

        if tags:

            try:
                tags = json.loads(tags)

                if isinstance(tags, dict):
                    tags = [tags]
                elif not isinstance(tags, list):
                    return action_result.set_status(
                        phantom.APP_ERROR,
                        "Invalid data format for tags, please enter data in valid format as mentioned in documentation"
                    )

                if isinstance(tags, list) and all(isinstance(x, dict) for x in tags):
                    pass
                else:
                    raise Exception
            except Exception:
                return action_result.set_status(
                    phantom.APP_ERROR, "Invalid Json data for tags")

            if len(tags) > 50:
                return action_result.set_status(
                    phantom.APP_ERROR,
                    "Limit crossed for maximum number of tags, at max 50 tags can be created"
                )

            tags_list = list()

            for data in tags:
                if 'Key' in data.keys() and 'Value' in data.keys():
                    tags_data = {
                        "Key": data.get("Key", ""),
                        "Value": data.get("Value", "")
                    }
                    tags_list.append(tags_data)
                else:
                    return action_result.set_status(
                        phantom.APP_ERROR,
                        "Could not parse data for tags, please enter data in valid format"
                    )
            payload["Tags"] = tags_list

        self.debug_print("Making Boto call")
        ret_val, resp = self._make_boto_call(
            action_result, "create_table", kwargs=payload)

        if (phantom.is_fail(ret_val)):
            return ret_val

        # converting datetime object to str
        resp = json.dumps(resp, default=str)
        resp = json.loads(resp)

        action_result.add_data(resp)
        return action_result.set_status(phantom.APP_SUCCESS, "Created Table successfully")

    def _delete_table(self, param):
        action_result = self.add_action_result(ActionResult(dict(param)))

        if not self._create_client(action_result, param):
            return action_result.get_status()

        table_name = param["table_name"]
        payload = {'TableName': table_name}

        self.debug_print("Making Boto call")
        ret_val, resp = self._make_boto_call(
            action_result, "delete_table", kwargs=payload)

        if (phantom.is_fail(ret_val)):
            return ret_val

        self.debug_print("Converting datetime object to string")
        resp = json.dumps(resp, default=str)
        resp = json.loads(resp)

        action_result.add_data(resp)
        return action_result.set_status(phantom.APP_SUCCESS, "Deleted Table Successfully")

    def _list_tables(self, param):
        """
        List all the available tables in the DynamoDB database
        """

        action_result = self.add_action_result(ActionResult(dict(param)))

        if not self._create_client(action_result, param):
            return action_result.get_status()

        payload = {'PaginationConfig': {}}
        ret_val, max_items = self._validate_integer(
            action_result,
            param.get('max_items'),
            "max items"
        )
        if (phantom.is_fail(ret_val)):
            return action_result.get_status()

        starting_token = param.get('starting_token')

        if max_items:
            payload['PaginationConfig']['MaxItems'] = max_items
        if starting_token:
            payload['PaginationConfig']['StartingToken'] = starting_token

        self.debug_print("Making Boto call")
        ret_val, resp = self._paginator(action_result, "list_tables", payload)

        if (phantom.is_fail(ret_val)):
            return ret_val

        # declaring varibales to store result data from pagination object
        table_list = list()
        result = dict()

        self.debug_print("Iterating over paginator object")
        # Iterating over paginator
        try:
            for data in resp:
                table_list.extend(data["TableNames"])
        except Exception as e:
            return action_result.set_status(phantom.APP_ERROR, 'boto3 call to Dynamodb failed : {}'.format(e))

        result['TableNames'] = table_list
        action_result.add_data(result)
        return action_result.set_status(phantom.APP_SUCCESS, "Fetched list of table successfully")

    def _describe_table(self, param):

        action_result = self.add_action_result(ActionResult(dict(param)))

        if not self._create_client(action_result, param):
            return action_result.get_status()

        table_name = param["table_name"]

        payload = {
            "TableName": table_name
        }

        self.debug_print("Making Boto call")
        ret_val, resp = self._make_boto_call(
            action_result,
            "describe_table",
            kwargs=payload
        )

        if (phantom.is_fail(ret_val)):
            return ret_val

        self.debug_print("converting datatime object to string")
        resp = json.dumps(resp, default=str)
        resp = json.loads(resp)

        action_result.add_data(resp)
        return action_result.set_status(phantom.APP_SUCCESS, "Table details fetched successfully")

    def _put_item(self, param):
        self.debug_print("Inside put item action")
        action_result = self.add_action_result(ActionResult(dict(param)))

        if not self._create_client(action_result, param):
            return action_result.get_status()

        table_name = param["table_name"]
        condition_expression = param.get('condition_expression')
        attribute_names = param.get('expression_attribute_names')
        attribute_values = param.get('expression_attribute_values')

        try:
            item_json = json.loads(param["item_json"])
        except Exception:
            return action_result.set_status(
                phantom.APP_ERROR,
                "Invalid format for expression Item Json, please enter data in correct format"
            )

        payload = {
            "TableName": table_name,
            "Item": item_json
        }

        if attribute_names and attribute_values:

            try:
                attribute_names = json.loads(attribute_names)
                if isinstance(attribute_names, dict):
                    payload['ExpressionAttributeNames'] = attribute_names
                else:
                    raise Exception
            except Exception:
                return action_result.set_status(
                    phantom.APP_ERROR,
                    "Invalid format for expression attribute names, please enter data in correct format"
                )

            try:
                attribute_values = json.loads(attribute_values)
                if isinstance(attribute_values, dict):
                    payload['ExpressionAttributeValues'] = attribute_values
                else:
                    raise Exception
            except Exception:
                return action_result.set_status(
                    phantom.APP_ERROR,
                    "Invalid format for expression attribute values, please enter data in correct format"
                )

        if condition_expression:
            payload['ConditionExpression'] = condition_expression

        self.debug_print("Making Boto call")
        ret_val, resp = self._make_boto_call(
            action_result,
            "put_item",
            kwargs=payload
        )

        if (phantom.is_fail(ret_val)):
            return ret_val

        action_result.add_data(resp)
        return action_result.set_status(phantom.APP_SUCCESS, "Item inserted successfully")

    def _get_item(self, param):

        action_result = self.add_action_result(ActionResult(dict(param)))

        if not self._create_client(action_result, param):
            return action_result.get_status()

        partition_key_name = param['partition_key_name']
        sort_key_name = param.get('sort_key_name')
        projection_expression = param.get('attributes_to_get', "")
        reserved_keyword = param.get('reserved_keyword_attributes', "")

        payload = {
            "TableName": param['table_name'],
            "Key": {
                partition_key_name: {
                    AWS_DYNAMODB_DATATYPES.get(param.get('partition_key_datatype').lower()): param.get('partition_key_value')
                }
            },
        }

        self.debug_print('checking for optional parameters')
        if sort_key_name:
            payload['Key'][sort_key_name] = {
                AWS_DYNAMODB_DATATYPES.get(param.get('sort_key_datatype').lower()): param.get('sort_key_value')
            }

        if projection_expression:
            payload['ProjectionExpression'] = projection_expression.strip(",")

        if reserved_keyword:
            payload['ExpressionAttributeNames'] = dict()
            reserved_keyword_list = self._handle_comma_separated_string(
                reserved_keyword)

            for index, keyword in enumerate(reserved_keyword_list):
                projection_expression += ",#n{}".format(index)
                payload["ExpressionAttributeNames"]["#n{}".format(
                    index)] = keyword

            payload['ProjectionExpression'] = projection_expression.strip(",")

        self.debug_print("Making Boto call")
        ret_val, resp = self._make_boto_call(
            action_result, "get_item", kwargs=payload)

        if (phantom.is_fail(ret_val)):
            return ret_val

        action_result.add_data(resp)
        return action_result.set_status(phantom.APP_SUCCESS, "Fetched Item Data Successfully")

    def _delete_item(self, param):

        action_result = self.add_action_result(ActionResult(dict(param)))

        if not self._create_client(action_result, param):
            return action_result.get_status()

        partition_key = param['partition_key']
        sort_key = param.get('sort_key')
        condition_expression = param.get('condition_expression')
        attribute_names = param.get('expression_attribute_names')
        attribute_values = param.get('expression_attribute_values')

        payload = {
            "TableName": param['table_name'],
            "Key": {
                partition_key: {
                    AWS_DYNAMODB_DATATYPES.get(param.get('partition_key_datatype').lower()): param.get('partition_key_value')
                }
            },
        }

        self.debug_print('checking for optional parameters')
        if sort_key:
            payload['Key'][sort_key] = {
                AWS_DYNAMODB_DATATYPES.get(param.get('sort_key_datatype').lower()): param.get('sort_key_value')
            }
        if condition_expression:
            payload['ConditionExpression'] = condition_expression
        if attribute_names and attribute_values:

            try:
                attribute_names = json.loads(attribute_names)
                if isinstance(attribute_names, dict):
                    payload['ExpressionAttributeNames'] = attribute_names
                else:
                    raise Exception
            except Exception:
                return action_result.set_status(
                    phantom.APP_ERROR,
                    "Invalid format for expression attribute names, please enter data in correct format"
                )

            try:
                attribute_values = json.loads(attribute_values)
                if isinstance(attribute_values, dict):
                    payload['ExpressionAttributeValues'] = attribute_values
                else:
                    raise Exception
            except Exception:
                return action_result.set_status(
                    phantom.APP_ERROR,
                    "Invalid format for expression attribute values, please enter data in correct format"
                )

        self.debug_print("Making Boto call")
        ret_val, resp = self._make_boto_call(
            action_result, "delete_item", kwargs=payload)

        if (phantom.is_fail(ret_val)):
            return ret_val

        action_result.add_data(resp)
        return action_result.set_status(phantom.APP_SUCCESS, "Item deleted successfully")

    def _update_item(self, param):
        """
        Update an item in the table
        """
        action_result = self.add_action_result(ActionResult(dict(param)))
        self.save_progress("Querying AWS to validate credentials")

        if not self._create_client(action_result, param):
            return action_result.get_status()

        table_name = param['table_name']
        partiton_key = param['partition_key']
        sort_key = param.get('sort_key')

        update_expression = param.get('update_expression')
        attribute_names = param.get('expression_attribute_names')
        attribute_values = param.get('expression_attribute_values')

        payload = {
            "TableName": table_name,
            "Key": {
                partiton_key: {
                    AWS_DYNAMODB_DATATYPES.get(param['partition_key_datatype'].lower()): param['partition_key_value']
                }
            }
        }

        self.debug_print('checking for optional parameters')
        if sort_key:
            sort_key_datatype = param.get('sort_key_datatype')
            sort_key_value = param.get('sort_key_value')
            if sort_key_datatype:
                sort_key_datatype = sort_key_datatype.lower()
            else:
                return action_result.set_status(phantom.APP_ERROR, "Missing sort key datatype, please enter a value for it")

            if sort_key_value:
                payload['Key'][sort_key] = {
                    AWS_DYNAMODB_DATATYPES.get(sort_key_datatype): sort_key_value}
            else:
                return action_result.set_status(phantom.APP_ERROR, "Missing sort key value, please enter a value for it")

        if update_expression:
            payload['UpdateExpression'] = update_expression

        if attribute_names and attribute_values:
            try:
                attribute_names = json.loads(attribute_names)
                if isinstance(attribute_names, dict):
                    payload['ExpressionAttributeNames'] = attribute_names
                else:
                    raise Exception
            except Exception:
                return action_result.set_status(
                    phantom.APP_ERROR,
                    "Invalid format for expression attribute names, please enter data in correct format"
                )

            try:
                attribute_values = json.loads(attribute_values)
                if isinstance(attribute_values, dict):
                    payload['ExpressionAttributeValues'] = attribute_values
                else:
                    raise Exception
            except Exception:
                return action_result.set_status(
                    phantom.APP_ERROR,
                    "Invalid format for expression attribute values, please enter data in correct format"
                )

        self.debug_print("Making Boto call")
        ret_val, resp = self._make_boto_call(
            action_result, "update_item", kwargs=payload)

        if phantom.is_fail(ret_val):
            return action_result.get_status()

        action_result.add_data(resp)
        return action_result.set_status(phantom.APP_SUCCESS, "Updated item successfully")

    def _query_data(self, param):
        action_result = self.add_action_result(ActionResult(dict(param)))

        if not self._create_client(action_result, param):
            return action_result.get_status()

        table_name = param['table_name']
        key_condition_expression = param['key_condition_expression']
        filter_expression = param.get('filter_expression')
        projection_expression = param.get('projection_expression')
        sort_descending = param.get('sort_descending')
        select = param.get('select')
        return_consumed_capacity = param.get('return_consumed_capacity')
        consistent_read = param.get('consistent_read')
        attribute_names = param.get('expression_attribute_names')
        attribute_values = param.get('expression_attribute_values')

        ret_val, max_items = self._validate_integer(
            action_result,
            param.get('max_items'),
            'max items'
        )
        if (phantom.is_fail(ret_val)):
            return action_result.get_status()

        exclusive_start_key = param.get('exclusive_start_key')

        payload = {
            "TableName": table_name,
            "KeyConditionExpression": key_condition_expression,
        }

        if attribute_names and attribute_values:
            try:
                attribute_names = json.loads(attribute_names)
                if isinstance(attribute_names, dict):
                    payload['ExpressionAttributeNames'] = attribute_names
                else:
                    raise Exception
            except Exception:
                return action_result.set_status(
                    phantom.APP_ERROR,
                    "Invalid format for expression attribute names, please enter data in correct format"
                )

            try:
                attribute_values = json.loads(attribute_values)
                if isinstance(attribute_values, dict):
                    payload['ExpressionAttributeValues'] = attribute_values
                else:
                    raise Exception
            except Exception:
                return action_result.set_status(
                    phantom.APP_ERROR,
                    "Invalid format for expression attribute values, please enter data in correct format"
                )

        # adding data for optional data
        self.debug_print("checking optional parameters")
        if select:
            payload["Select"] = select
        if max_items:
            payload['PaginationConfig']['MaxItems'] = max_items
        if filter_expression:
            payload["FilterExpression"] = filter_expression
        if sort_descending:
            payload["ScanIndexForward"] = not sort_descending
        if projection_expression:
            payload["ProjectionExpression"] = projection_expression
            payload["Select"] = "SPECIFIC_ATTRIBUTES"
        if consistent_read:
            payload['ConsistentRead'] = consistent_read
        if exclusive_start_key:
            payload['ExclusiveStartKey'] = exclusive_start_key
        if return_consumed_capacity:
            payload['ReturnConsumedCapacity'] = return_consumed_capacity

        self.debug_print("Making Boto call")
        ret_val, resp = self._paginator(action_result, "query", payload)

        if phantom.is_fail(ret_val):
            return action_result.get_status()
        data_list = []
        last_evaluated_key = dict()
        result = dict()
        try:
            for data in resp:
                self.debug_print(data)
                data_list.extend(data['Items'])
                if data.get('LastEvaluatedKey'):
                    last_evaluated_key = data['LastEvaluatedKey']
        except Exception as e:
            return action_result.set_status(phantom.APP_ERROR, 'boto3 call to Dynamodb failed : {}'.format(e))

        result['Items'] = data_list
        if last_evaluated_key:
            result['Last_evaluated_key'] = last_evaluated_key
        action_result.add_data(result)
        return action_result.set_status(phantom.APP_SUCCESS, "Fetched data successfully")

    def _create_backup(self, param):
        action_result = self.add_action_result(ActionResult(dict(param)))

        if not self._create_client(action_result, param):
            return action_result.get_status()

        table_name = param["table_name"]
        backup_name = param["backup_name"]

        payload = {"BackupName": backup_name, "TableName": table_name}

        self.debug_print("Making Boto call")
        ret_val, resp = self._make_boto_call(
            action_result, "create_backup", kwargs=payload
        )

        if phantom.is_fail(ret_val):
            return ret_val

        self.debug_print("converting datatime object to string")
        resp = json.dumps(resp, default=str)
        resp = json.loads(resp)

        action_result.add_data(resp)
        return action_result.set_status(phantom.APP_SUCCESS, "Created backup successfully")

    def _delete_backup(self, param):
        action_result = self.add_action_result(ActionResult(dict(param)))

        if not self._create_client(action_result, param):
            return action_result.get_status()

        backup_arn = param["backup_arn"]

        payload = {"BackupArn": backup_arn}

        self.debug_print("Making Boto call")
        ret_val, resp = self._make_boto_call(
            action_result, "delete_backup", kwargs=payload
        )

        if phantom.is_fail(ret_val):
            return ret_val

        self.debug_print("converting datatime object to string")
        resp = json.dumps(resp, default=str)
        resp = json.loads(resp)

        action_result.add_data(resp)
        return action_result.set_status(phantom.APP_SUCCESS, "Deleted backup successfully")

    def _describe_backup(self, param):

        action_result = self.add_action_result(ActionResult(dict(param)))

        if not self._create_client(action_result, param):
            return action_result.get_status()

        backup_arn = param["backup_arn"]

        payload = {
            "BackupArn": backup_arn
        }

        self.debug_print("Making Boto call")
        ret_val, resp = self._make_boto_call(
            action_result,
            "describe_backup",
            kwargs=payload
        )

        if (phantom.is_fail(ret_val)):
            return ret_val

        self.debug_print("converting datatime object to string")
        resp = json.dumps(resp, default=str)
        resp = json.loads(resp)

        action_result.add_data(resp)
        return action_result.set_status(phantom.APP_SUCCESS, "Table details fetched successfully")

    def check_for_future_datetime(self, datetime_obj):
        """
        Check the given datetime str is a future date or not.

        :param datetime_obj: datetime object
        :return : bool
        """
        return datetime_obj > datetime.now()

    def _check_starttime_greater_than_endtime(self, datetime_start, datetime_end):
        """
        Check if the starttime is greater than endtime or not.

        :param datetime_start: start datetime
        :param datetime_end: end datetime
        :return : bool
        """
        return datetime_start > datetime_end

    def _parse_and_validate_date(self, dt_str, action_result, key):
        """
        Convert input date to iso8601 datetime.

        :param dt_str: datetime string
        :param action_result: action result object
        :param key: input parameter key
        :return : status and datetime object
        """
        try:
            datetime.strptime(dt_str, "%Y/%m/%d")
        except Exception:
            return (
                action_result.set_status(
                    phantom.APP_ERROR,
                    "Invalid date format please enter date in (YYYY/MM/DD) format"
                ),
                None,
            )
        try:
            date_time = parse(dt_str)
            time_stamp = date_time.timestamp()
            if self.check_for_future_datetime(date_time):
                return (
                    action_result.set_status(
                        phantom.APP_ERROR,
                        "The provided date is a future datetime. Please provide a valid value for parameter '{}'".format(
                            key
                        ),
                    ),
                    None,
                )

        except Exception:
            return (
                action_result.set_status(
                    phantom.APP_ERROR, "Parameter '{}' is invalid".format(key)
                ),
                None,
            )
        return (phantom.APP_SUCCESS, time_stamp)

    def _list_backups(self, param):
        action_result = self.add_action_result(ActionResult(dict(param)))

        if not self._create_client(action_result, param):
            return action_result.get_status()

        backup_type = param.get("backup_type")
        exclusive_start_backup_arn = param.get("exclusive_start_backup_arn")
        ret_val, max_items = self._validate_integer(
            action_result,
            param.get("max_items"),
            'max items'
        )
        if (phantom.is_fail(ret_val)):
            return action_result.get_status()

        table_name = param.get("table_name")
        time_range_lower_bound = param.get("start_date")
        time_range_upper_bound = param.get("end_date")

        payload = {'PaginationConfig': {}}

        self.debug_print("checking optional parameters")
        if backup_type:
            payload['BackupType'] = backup_type
        if exclusive_start_backup_arn:
            payload['PaginationConfig']['StartingToken'] = exclusive_start_backup_arn

        if max_items:
            payload['PaginationConfig']['MaxItems'] = max_items
        if table_name:
            payload['TableName'] = table_name
        if time_range_lower_bound:
            retval, time_range_lower_bound = self._parse_and_validate_date(
                time_range_lower_bound, action_result, "start date")

            if phantom.is_fail(retval):
                return action_result.get_status()

            self.debug_print(time_range_lower_bound)

            payload['TimeRangeLowerBound'] = time_range_lower_bound
        if time_range_upper_bound:
            retval, time_range_upper_bound = self._parse_and_validate_date(
                time_range_upper_bound, action_result, "end date")
            if phantom.is_fail(retval):
                return action_result.get_status()

            self.debug_print(time_range_upper_bound)

            payload['TimeRangeUpperBound'] = time_range_upper_bound

        if time_range_lower_bound and time_range_upper_bound:
            if self._check_starttime_greater_than_endtime(time_range_lower_bound, time_range_upper_bound):
                return action_result.set_status(phantom.APP_ERROR, "The upper bound value must be greater than lower bound value")

        self.debug_print("Making Boto call")
        ret_val, resp = self._paginator(action_result, "list_backups", payload)

        if phantom.is_fail(ret_val):
            return ret_val
        try:
            for data in resp:
                response = json.dumps(data, default=str)
                response = json.loads(response)
                action_result.add_data(response)
        except Exception as e:
            return action_result.set_status(phantom.APP_ERROR, 'boto3 call to Dynamodb failed : {}'.format(e))

        return action_result.set_status(phantom.APP_SUCCESS, "Fetched backup data successfully")

    def _restore_table_from_backup(self, param):
        action_result = self.add_action_result(ActionResult(dict(param)))

        if not self._create_client(action_result, param):
            return action_result.get_status()

        table_name = param["table_name"]
        backup_arn = param["backup_arn"]
        billing_mode_override = param.get("billing_mode_override")
        read_capacity_override = param.get("read_capacity_override", 5)
        write_capacity_override = param.get("write_capacity_override", 5)
        restore_secondary_indexes = param["restore_secondary_indexes"]
        sse = param.get("sse_enable_override")
        kms_master_key_id = param.get("kms_master_key_id")

        payload = {
            "TargetTableName": table_name,
            "BackupArn": backup_arn,
        }

        if billing_mode_override:
            payload["BillingModeOverride"] = billing_mode_override
            if billing_mode_override == "PROVISIONED":
                payload["ProvisionedThroughputOverride"] = {
                    'ReadCapacityUnits': read_capacity_override,
                    'WriteCapacityUnits': write_capacity_override
                }

        if restore_secondary_indexes == "Restore without secondary indexes":
            payload["GlobalSecondaryIndexes"] = []
            payload["LocalSecondaryIndexes"] = []

        if sse == "True":
            payload["SSESpecificationOverride"] = {
                "Enabled": True,
                "SSEType": "KMS"
            }
            if kms_master_key_id:
                payload["SSESpecificationOverride"] = {
                    "KMSMasterKeyId": kms_master_key_id
                }
        elif sse == "False":
            payload["SSESpecificationOverride"] = {
                "Enabled": False
            }

        self.debug_print("Making Boto call")
        ret_val, resp = self._make_boto_call(
            action_result, "restore_table_from_backup", kwargs=payload
        )

        if phantom.is_fail(ret_val):
            return ret_val

        self.debug_print("converting datatime object to string")
        resp = json.dumps(resp, default=str)
        resp = json.loads(resp)

        action_result.add_data(resp)
        return action_result.set_status(phantom.APP_SUCCESS, "Restored backup from table successfully")

    def _create_global_table(self, param):
        action_result = self.add_action_result(ActionResult(dict(param)))

        if not self._create_client(action_result, param):
            return action_result.get_status()

        global_table_name = param["global_table_name"]
        replication_group = self._handle_comma_separated_string(
            param["replication_group"])

        payload = {
            "GlobalTableName": global_table_name,
            "ReplicationGroup": [
                {
                    'RegionName': region
                } for region in replication_group
            ]
        }

        self.debug_print("Making Boto call")
        ret_val, resp = self._make_boto_call(
            action_result, "create_global_table", kwargs=payload
        )

        if phantom.is_fail(ret_val):
            return ret_val

        self.debug_print("converting datetime object to string")
        resp = json.dumps(resp, default=str)
        resp = json.loads(resp)

        action_result.add_data(resp)
        return action_result.set_status(phantom.APP_SUCCESS, "Created global table successfully")

    def _list_global_tables(self, param):
        action_result = self.add_action_result(ActionResult(dict(param)))

        if not self._create_client(action_result, param):
            return action_result.get_status()

        global_table_name = param.get("global_table_name")
        region_name = param.get("region_name")
        ret_val, limit = self._validate_integer(
            action_result,
            param.get("limit"),
            'limit'
        )

        if (phantom.is_fail(ret_val)):
            return action_result.get_status()

        payload = dict()

        if global_table_name:
            payload["ExclusiveStartGlobalTableName"] = global_table_name

        if region_name:
            payload["RegionName"] = region_name

        if limit:
            payload["Limit"] = limit

        self.debug_print("Making Boto call")
        ret_val, resp = self._make_boto_call(
            action_result, "list_global_tables", kwargs=payload
        )

        if phantom.is_fail(ret_val):
            return ret_val

        self.debug_print("converting datetime object to string")
        resp = json.dumps(resp, default=str)
        resp = json.loads(resp)

        action_result.add_data(resp)
        return action_result.set_status(phantom.APP_SUCCESS, "Fetched global table list successfully")

    def _describe_global_table(self, param):

        action_result = self.add_action_result(ActionResult(dict(param)))

        if not self._create_client(action_result, param):
            return action_result.get_status()

        global_table_name = param["global_table_name"]

        payload = {
            "GlobalTableName": global_table_name
        }

        self.debug_print("Making Boto call")
        ret_val, resp = self._make_boto_call(
            action_result,
            "describe_global_table",
            kwargs=payload
        )

        if (phantom.is_fail(ret_val)):
            return ret_val

        self.debug_print("converting datatime object to string")
        resp = json.dumps(resp, default=str)
        resp = json.loads(resp)

        action_result.add_data(resp)
        return action_result.set_status(phantom.APP_SUCCESS, "Table details fetched successfully")

    def _handle_test_connectivity(self, param):
        """
        Check asset connectivity with the application platform
        """

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))
        self.save_progress("Querying AWS to validate credentials")

        if not self._create_client(action_result, param):
            return action_result.get_status()

        payload = {'PaginationConfig': {'MaxItems': 2}}

        ret_val, resp = self._paginator(action_result, "list_tables", payload)

        if phantom.is_fail(ret_val):
            self.save_progress("Test Connectivity Failed")
            return action_result.get_status()

        self.save_progress("Test Connectivity Passed")
        return action_result.set_status(phantom.APP_SUCCESS)

    def handle_action(self, param):
        ret_val = phantom.APP_SUCCESS

        # Get the action that we are supposed to execute for this App Run
        action_id = self.get_action_identifier()

        self.debug_print("action_id", self.get_action_identifier())

        if action_id == 'test_connectivity':
            ret_val = self._handle_test_connectivity(param)
        elif action_id == 'create_table':
            ret_val = self._create_table(param)
        elif action_id == 'list_tables':
            ret_val = self._list_tables(param)
        elif action_id == 'delete_table':
            ret_val = self._delete_table(param)
        elif action_id == "put_item":
            ret_val = self._put_item(param)
        elif action_id == "get_item":
            ret_val = self._get_item(param)
        elif action_id == "delete_item":
            ret_val = self._delete_item(param)
        elif action_id == "update_item":
            ret_val = self._update_item(param)
        elif action_id == "query_data":
            ret_val = self._query_data(param)
        elif action_id == "delete_backup":
            ret_val = self._delete_backup(param)
        elif action_id == "create_backup":
            ret_val = self._create_backup(param)
        elif action_id == "list_backups":
            ret_val = self._list_backups(param)
        elif action_id == "create_global_table":
            ret_val = self._create_global_table(param)
        elif action_id == "list_global_tables":
            ret_val = self._list_global_tables(param)
        elif action_id == "restore_table_from_backup":
            ret_val = self._restore_table_from_backup(param)
        elif action_id == "describe_table":
            ret_val = self._describe_table(param)
        elif action_id == "describe_backup":
            ret_val = self._describe_backup(param)
        elif action_id == "describe_global_table":
            ret_val = self._describe_global_table(param)
        return ret_val


def main():
    import argparse

    argparser = argparse.ArgumentParser()

    argparser.add_argument('input_test_json', help='Input Test JSON file')
    argparser.add_argument(
        '-u', '--username', help='username', required=False)
    argparser.add_argument(
        '-p', '--password', help='password', required=False)

    args = argparser.parse_args()
    session_id = None

    username = args.username
    password = args.password

    if username is not None and password is None:
        # User specified a username but not a password, so ask
        import getpass
        password = getpass.getpass("Password: ")

    if username and password:
        try:
            login_url = AwsDynamodbConnector._get_phantom_base_url() + '/login'

            print("Accessing the Login page")
            r = requests.get(login_url, verify=False)
            csrftoken = r.cookies['csrftoken']

            data = dict()
            data['username'] = username
            data['password'] = password
            data['csrfmiddlewaretoken'] = csrftoken

            headers = dict()
            headers['Cookie'] = 'csrftoken=' + csrftoken
            headers['Referer'] = login_url

            print("Logging into Platform to get the session id")
            r2 = requests.post(login_url, verify=False,
                               data=data, headers=headers)
            session_id = r2.cookies['sessionid']
        except Exception as e:
            print("Unable to get session id from the platform. Error: " + str(e))
            exit(1)

    with open(args.input_test_json) as f:
        in_json = f.read()
        in_json = json.loads(in_json)
        print(json.dumps(in_json, indent=4))

        connector = AwsDynamodbConnector()
        connector.print_progress_message = True

        if session_id is not None:
            in_json['user_session_token'] = session_id
            connector._set_csrf_info(csrftoken, headers['Referer'])

        ret_val = connector._handle_action(json.dumps(in_json), None)
        print(json.dumps(json.loads(ret_val), indent=4))

    exit(0)


if __name__ == '__main__':
    main()
