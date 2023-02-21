[comment]: # "Auto-generated SOAR connector documentation"
# AWS DynamoDB

Publisher: Splunk  
Connector Version: 1\.0\.0  
Product Vendor: AWS  
Product Name: AWS DynamoDB  
Product Version Supported (regex): "\.\*"  
Minimum Product Version: 5\.4\.0  

This app supports CRUD operations in a AWS DynamoDB database

[comment]: # " File: README.md"
[comment]: # "  Copyright (c) 2023 Splunk Inc."
[comment]: # ""
[comment]: # "Licensed under the Apache License, Version 2.0 (the 'License');"
[comment]: # "you may not use this file except in compliance with the License."
[comment]: # "You may obtain a copy of the License at"
[comment]: # ""
[comment]: # "    http://www.apache.org/licenses/LICENSE-2.0"
[comment]: # ""
[comment]: # "Unless required by applicable law or agreed to in writing, software distributed under"
[comment]: # "the License is distributed on an 'AS IS' BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,"
[comment]: # "either express or implied. See the License for the specific language governing permissions"
[comment]: # "and limitations under the License."
[comment]: # ""
<div style="margin-left: 2em">

### Expressions in DynamoDB

AWS DynamoDBuse uses expressions to denote the attributes that you want to read from an item. It
also uses expressions when writing an item to indicate any conditions that must be met, and to
indicate how the attributes are to be updated. Expressions are an integral part of using DynamoDB,
and they are used in a few different ways:

- #### Condition Expressions

  To manipulate data in an AWS DynamoDB table, we use the Put Item, Update Item, and Delete Item
  operation. For these data manipulation operations, we can specify a condition expression to
  determine which items should be modified. If the condition expression evaluates to true, the
  operation succeeds; otherwise, the operation fails.

- #### Update Expressions

  To update an existing item in an AWS DynamoDB table, we use the Update Item operation. We must
  provide the key of the item that we want to update. We must also provide an update expression,
  indicating the attributes that you want to modify and the values that you want to assign to them.
  There are 4 operations update expression suppports :

  - <a
    href="https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Expressions.UpdateExpressions.html#Expressions.UpdateExpressions.SET"
    target="_blank">SET</a> —modifying or adding item attributes
  - <a
    href="https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Expressions.UpdateExpressions.html#Expressions.UpdateExpressions.REMOVE"
    target="_blank">REMOVE</a> —deleting attributes from an item
  - <a
    href="https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Expressions.UpdateExpressions.html#Expressions.UpdateExpressions.ADD"
    target="_blank">ADD</a> —updating numbers and sets
  - <a
    href="https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Expressions.UpdateExpressions.html#Expressions.UpdateExpressions.DELETE"
    target="_blank">DELETE</a> —removing elements from a set

- #### Key Condition Expressions

  They are used when querying a table with a composite primary key to limit the items selected.

- #### Filter Expressions

  They allow you to filter the results of queries and scans to allow for more efficient responses.

- #### Projection Expressions

  They are used to specify a subset of attributes you want to receive when reading Items. We used
  these in our GetItem calls in the previous lesson.



  



The following actions uses expressions



<table>
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<thead>
<tr class="header">
<th>Expression Name</th>
<th>Action Name</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>Condition Expression</td>
<td><ul>
<li>Delete Item</li>
<li>Put Item</li>
</ul></td>
</tr>
<tr class="even">
<td>Update Expression</td>
<td><ul>
<li>Update Item</li>
</ul></td>
</tr>
<tr class="odd">
<td>Key Condition Expression</td>
<td><ul>
<li>Query Data</li>
</ul></td>
</tr>
<tr class="even">
<td>Filter Expression</td>
<td><ul>
<li>Query Data</li>
</ul></td>
</tr>
<tr class="odd">
<td>Projection Expression</td>
<td><ul>
<li>Query Data</li>
</ul></td>
</tr>
</tbody>
</table>

#### Expression attribute names and values

While using this app certain actions will ask for **expression attribute names** and **expression
attributevalues** which would be neccessay while using expressions. This values are neccessay to
pass for the following conditions:

- To access an attribute whose name conflicts with a DynamoDB
  <a href="https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ReservedWords.html"
  target="_blank">reserved words</a> .
- To create a placeholder for repeating occurrences of an attribute name in an expression.
- To prevent special characters in an attribute name from being misinterpreted in an expression.

  



#### To write the expression attribute data reffer the code snippets given below



**Expression Attribute Names Syntax**

            {
              "#variable_key_name" : "actual_key_name"
            }
        

**Expression Attribute Names Example**

            {
              "#name":"name"
              "#age" : "age"
            }
        



  



**Expression Attribute Values Syntax**

            {
              ":variable_value_name" : {
                "datatype":"value_to_be_assigned"
              }
            }
        

**Expression Attribute Values Example**

            {
              ":name": {
                  "S":"Jhon Doe"
              },
              ":age":{
                  "N":"22"
              }
            }
        







**Local Secondary Index**

To create a local secondary index(LSI), sort key becomes necessary. The partition key remains the
same as that of the table If you want to make single local secondary index takes, just pass a JSON
object with the attributes given below and for multiple local secondary indexes pass an array of
JSON objects.(Can only create 5 LSI at max)

- Key name: **sort_key_name**

  Description: Name of the local secondary sort key

  Required: True

  Input Type: String

- Key name: **sort_key_datatype**

  Description: Datatype for the local secondary sort key (accepts only 3 types of values as valid,
  that are **String, Number or Binary** )

  Required: True

  Input Type: String

- Key name: **attribute_projection**

  Description: Type of attribute projection. There are the following types of projections

  - KEYS_ONLY: Only the index and primary keys are projected into the index.
  - INCLUDE: Only the specified table attributes are projected into the index. The list of projected
    attributes is in NonKeyAttributes .
  - ALL: All of the table attributes are projected into the index.

  Required: True

  Input Type: String

- Key name: **non_key_attributes**

  Description: A list of one or more non-key attribute names that are projected into the secondary
  index. (Required only when the projection mode is set to INCLUDE)

  Required: False

  Input Type: Array of string values



VALUE EXAMPLE

- Single JSON object for LSI

                  {
                    "sort_key_name": "lsi_one",
                    "sort_key_datatype": "String",
                    "attribute_projection": "INCLUDE",
                    "non_key_attributes": [
                        "one",
                        "two",
                        "three"
                    ]
                  }
              

- Multiple JSON object for LSI

                  [
                    {
                        "sort_key_name": "lsi_one",
                        "sort_key_datatype": "String",
                        "attribute_projection": "INCLUDE",
                        "non_key_attributes": [
                            "one",
                            "two",
                            "three"
                        ]
                    },
                    {
                        "sort_key_name": "lsi_two",
                        "sort_key_datatype": "String",
                        "attribute_projection": "ALL",
                    }
                  ]
              







**Global Secondary Index**

To create a global secondary index(GSI), partition key becomes necessary. Sort key is optional. the
parameters for Global Secondary Indexes remain the same as Local Secondary Index, just Partition key
name and Partition key name datatype are added and they become required parameters. Whereas Sort key
name and Sort key datatype become optional. The provisional read and write capacity units are the
same as the original table.(Can only create 20 GSI at max)

- Key name: **partition_key_name**

  Description: Name of the local secondary sort key

  Required: True

  Input Type: String

- Key name: **partiton_key_datatype**

  Description: Datatype for the local secondary sort key (accepts only 3 types of values as valid,
  that are **String, Number or Binary** )

  Required: True

  Input Type: String

- Key name: **sort_key_name**

  Description: Name of the global secondary sort key (required parameter)

  Required: False

  Input Type: String

- Key name: **sort_key_datatype**

  Description: Datatype for the global secondary sort key (accepts only 3 types of values as valid,
  that are **String, Number or Binary** )

  Required: False

  Input Type: String

- Key name: **attribute_projection**

  Description: Type of attribute projection. There are the following types of projections

  - KEYS_ONLY: Only the index and primary keys are projected into the index.
  - INCLUDE: Only the specified table attributes are projected into the index. The list of projected
    attributes is in NonKeyAttributes .
  - ALL: All of the table attributes are projected into the index.

  Required: True

  Input Type: String

- Key name: **non_key_attributes**

  Description: A list of one or more non-key attribute names that are projected into the secondary
  index. (Required only when the projection mode is set to INCLUDE)

  Required: False

  Input Type: Array of string values



VALUE EXAMPLE

- Single JSON object for GSI

                  {
                    "partition_key_name": "gsi_id",
                    "partition_key_datatype": "Number",
                    "sort_key_name": "gsi_one",
                    "sort_key_datatype": "String",
                    "attribute_projection": "INCLUDE",
                    "non_key_attributes": [
                        "one",
                        "two",
                        "three"
                    ]
                  }
              

- Multiple JSON object for GSI

                  [
                    {
                        "partition_key_name": "gsi_id",
                        "partition_key_datatype": "Number",
                        "sort_key_name": "gsi_one",
                        "sort_key_datatype": "String",
                        "attribute_projection": "INCLUDE",
                        "non_key_attributes": [
                            "one",
                            "two",
                            "three"
                        ]
                    },
                    {
                        "partition_key_name": "gsi_name",
                        "partition_key_datatype": "String",
                        "attribute_projection": "ALL",
                    }
                  ]
              







#### Available AWS Regions

|                           |                |
|---------------------------|----------------|
| REGION NAME               | REGION         |
| US East (Ohio)            | us-east-2      |
| US East (N. Virginia)     | us-east-1      |
| US West (N. California)   | us-west-1      |
| US West (Oregon)          | us-west-2      |
| Africa (Cape Town)        | af-south-1     |
| Asia Pacific (Hong Kong)  | ap-east-1      |
| Asia Pacific (Hyderabad)  | ap-south-2     |
| Asia Pacific (Jakarta)    | ap-southeast-3 |
| Asia Pacific (Mumbai)     | ap-south-1     |
| Asia Pacific (Osaka)      | ap-northeast-3 |
| Asia Pacific (Seoul)      | ap-northeast-2 |
| Asia Pacific (Singapore)  | ap-southeast-1 |
| Asia Pacific (Sydney)     | ap-southeast-2 |
| Asia Pacific (Tokyo)      | ap-northeast-1 |
| Canada (Central)          | ca-central-1   |
| Europe (Frankfurt)        | eu-central-1   |
| Europe (Ireland)          | eu-west-1      |
| Europe (London)           | eu-west-2      |
| Europe (Milan)            | eu-south-1     |
| Europe (Paris)            | eu-west-3      |
| Europe (Spain)            | eu-south-2     |
| Europe (Stockholm)        | eu-north-1     |
| Europe (Zurich)           | eu-central-2   |
| Middle East (Bahrain)     | me-south-1     |
| Middle East (UAE)         | me-central-1   |
| South America (São Paulo) | sa-east-1      |
| AWS GovCloud (US-East)    | us-gov-east-1  |
| AWS GovCloud (US-West)    | us-gov-west-1  |




### Configuration Variables
The below configuration variables are required for this Connector to operate.  These variables are specified when configuring a AWS DynamoDB asset in SOAR.

VARIABLE | REQUIRED | TYPE | DESCRIPTION
-------- | -------- | ---- | -----------
**access\_key** |  optional  | password | Access Key
**secret\_key** |  optional  | password | Secret Key
**region** |  required  | string | Region
**use\_role** |  optional  | boolean | Use attached role when running Phantom in EC2

### Supported Actions  
[describe global table](#action-describe-global-table) - Fetch metadata of a global table  
[describe backup](#action-describe-backup) - Fetch metadata of a backup  
[describe table](#action-describe-table) - Fetch metadata of a table  
[create global table](#action-create-global-table) - Create a global table from an existing table in the specified region l  
[list global tables](#action-list-global-tables) - List all global tables that have a replica in the specified Region  
[list backups](#action-list-backups) - List all the backups present in the database  
[delete backup](#action-delete-backup) - Delete backup of a table  
[create backup](#action-create-backup) - Create a backup of an existing table  
[restore backup table](#action-restore-backup-table) - Create a new table from an existing backup  
[list tables](#action-list-tables) - List all the tables present in the database  
[delete table](#action-delete-table) - Delete a table from the database  
[create table](#action-create-table) - Create a table in the database  
[delete item](#action-delete-item) - Delete an item from the table  
[put item](#action-put-item) - Add an item to the table  
[update item](#action-update-item) - Update an item in the table  
[get item](#action-get-item) - Get an item from the table  
[query data](#action-query-data) - Query data from database  
[test connectivity](#action-test-connectivity) - Validate the asset configuration for connectivity using the supplied configuration  

## action: 'describe global table'
Fetch metadata of a global table

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**global\_table\_name** |  required  | Name of Global Table | string | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action\_result\.status | string |  |   success  failed 
action\_result\.parameter\.global\_table\_name | string |  |   room 
action\_result\.parameter\.credentials | string |  `aws credentials`  |   \{'AccessKeyId'\: 'ASIASJL6ZZZZZ3M7QC2J', 'Expiration'\: '2021\-06\-07 22\:28\:04', 'SecretAccessKey'\: 'ZZZZZAmvLPictcVBPvjJx0d7MRezOuxiLCMZZZZZ', 'SessionToken'\: 'ZZZZZXIvYXdzEN///////////wEaDFRU0s4AVrw0k0oYICK4ATAzOqzAkg9bHY29lYmP59UvVOHjLufOy4s7SnAzOxGqGIXnukLis4TWNhrJl5R5nYyimrm6K/9d0Cw2SW9gO0ZRjEJHWJ\+yY5Qk2QpWctS2BGn4n\+G8cD6zEweCCMj\+ScI5p8n7YI4wOdvXvOsVMmjV6F09Ujqr1w\+NwoKXlglznXGs/7Q1kNZOMiioEhGUyoiHbQb37GCKslDK\+oqe0KNaUKQ96YCepaLgMbMquDgdAM8I0TTxUO0o5ILF/gUyLT04R7QlOfktkdh6Qt0atTS\+xeKi1hirKRizpJ8jjnxGQIikPRToL2v3ZZZZZZ=='\}  # pragma: allowlist secret
action\_result\.data\.\*\.Table | string |  |  
action\_result\.data\.\*\.Table\.TableName | string |  |  
action\_result\.data\.\*\.ResponseMetadata\.RequestId | string |  |   IVODR6MSFJFABNQ92LLHFE1BVJVV4KQNSO5AEMVJF66Q9ASUAAJG 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.date | string |  |   Thu, 16 Feb 2023 10\:15\:09 GMT 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.server | string |  |   Server 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.connection | string |  |   keep\-alive 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.x\-amz\-crc32 | string |  |   3053811167 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-type | string |  |   application/x\-amz\-json\-1\.0 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-length | string |  |   252 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.x\-amzn\-requestid | string |  |   IVODR6MSFJFABNQ92LLHFE1BVJVV4KQNSO5AEMVJF66Q9ASUAAJG 
action\_result\.data\.\*\.ResponseMetadata\.RetryAttempts | numeric |  |  
action\_result\.data\.\*\.ResponseMetadata\.HTTPStatusCode | numeric |  |   200 
action\_result\.data\.\*\.GlobalTableDescription\.GlobalTableArn | string |  |   arn\:aws\:dynamodb\:\:157568067690\:global\-table/test\_playbook 
action\_result\.data\.\*\.GlobalTableDescription\.GlobalTableName | string |  |   test\_playbook 
action\_result\.data\.\*\.GlobalTableDescription\.CreationDateTime | string |  |   2023\-02\-16 10\:15\:08\.116000\+00\:00 
action\_result\.data\.\*\.GlobalTableDescription\.ReplicationGroup\.\*\.RegionName | string |  |   us\-east\-1 
action\_result\.data\.\*\.GlobalTableDescription\.GlobalTableStatus | string |  |   ACTIVE 
action\_result\.message | string |  |   Created global table successfully 
action\_result\.summary | string |  |  
summary\.total\_objects | numeric |  |   1 
summary\.total\_objects\_successful | numeric |  |   1   

## action: 'describe backup'
Fetch metadata of a backup

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**backup\_arn** |  required  | Backup ARN string | string |  `aws dynamodb backup arn` 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action\_result\.status | string |  |   success  failed 
action\_result\.parameter\.backup\_arn | string |  `aws dynamodb backup arn`  |   room 
action\_result\.parameter\.credentials | string |  `aws credentials`  |   \{'AccessKeyId'\: 'ASIASJL6ZZZZZ3M7QC2J', 'Expiration'\: '2021\-06\-07 22\:28\:04', 'SecretAccessKey'\: 'ZZZZZAmvLPictcVBPvjJx0d7MRezOuxiLCMZZZZZ', 'SessionToken'\: 'ZZZZZXIvYXdzEN///////////wEaDFRU0s4AVrw0k0oYICK4ATAzOqzAkg9bHY29lYmP59UvVOHjLufOy4s7SnAzOxGqGIXnukLis4TWNhrJl5R5nYyimrm6K/9d0Cw2SW9gO0ZRjEJHWJ\+yY5Qk2QpWctS2BGn4n\+G8cD6zEweCCMj\+ScI5p8n7YI4wOdvXvOsVMmjV6F09Ujqr1w\+NwoKXlglznXGs/7Q1kNZOMiioEhGUyoiHbQb37GCKslDK\+oqe0KNaUKQ96YCepaLgMbMquDgdAM8I0TTxUO0o5ILF/gUyLT04R7QlOfktkdh6Qt0atTS\+xeKi1hirKRizpJ8jjnxGQIikPRToL2v3ZZZZZZ=='\}  # pragma: allowlist secret
action\_result\.data\.\*\.Table | string |  |  
action\_result\.data\.\*\.Table\.TableName | string |  |  
action\_result\.data\.\*\.ResponseMetadata\.RequestId | string |  |   M2M76PL4BOD12BK61IEUN1604VVV4KQNSO5AEMVJF66Q9ASUAAJG 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.date | string |  |   Thu, 16 Feb 2023 10\:15\:13 GMT 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.server | string |  |   Server 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.connection | string |  |   keep\-alive 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.x\-amz\-crc32 | string |  |   3983538543 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-type | string |  |   application/x\-amz\-json\-1\.0 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-length | string |  |   2043 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.x\-amzn\-requestid | string |  |   M2M76PL4BOD12BK61IEUN1604VVV4KQNSO5AEMVJF66Q9ASUAAJG 
action\_result\.data\.\*\.ResponseMetadata\.RetryAttempts | numeric |  |  
action\_result\.data\.\*\.ResponseMetadata\.HTTPStatusCode | numeric |  |   200 
action\_result\.data\.\*\.BackupDescription\.BackupDetails\.BackupArn | string |  |   arn\:aws\:dynamodb\:us\-east\-1\:157568067690\:table/test\_playbook/backup/01676542512426\-8ea20723 
action\_result\.data\.\*\.BackupDescription\.BackupDetails\.BackupName | string |  |   test\_playbook\_backup 
action\_result\.data\.\*\.BackupDescription\.BackupDetails\.BackupType | string |  |   USER 
action\_result\.data\.\*\.BackupDescription\.BackupDetails\.BackupStatus | string |  |   AVAILABLE 
action\_result\.data\.\*\.BackupDescription\.BackupDetails\.BackupSizeBytes | numeric |  |  
action\_result\.data\.\*\.BackupDescription\.BackupDetails\.BackupCreationDateTime | string |  |   2023\-02\-16 10\:15\:12\.426000\+00\:00 
action\_result\.data\.\*\.BackupDescription\.SourceTableDetails\.TableId | string |  |   291c7a8f\-8c39\-4727\-8ab6\-4a078eca09ce 
action\_result\.data\.\*\.BackupDescription\.SourceTableDetails\.TableArn | string |  |   arn\:aws\:dynamodb\:us\-east\-1\:157568067690\:table/test\_playbook 
action\_result\.data\.\*\.BackupDescription\.SourceTableDetails\.ItemCount | numeric |  |  
action\_result\.data\.\*\.BackupDescription\.SourceTableDetails\.KeySchema\.\*\.KeyType | string |  |   HASH 
action\_result\.data\.\*\.BackupDescription\.SourceTableDetails\.KeySchema\.\*\.AttributeName | string |  |   test\_part\_key 
action\_result\.data\.\*\.BackupDescription\.SourceTableDetails\.TableName | string |  |   test\_playbook 
action\_result\.data\.\*\.BackupDescription\.SourceTableDetails\.BillingMode | string |  |   PROVISIONED 
action\_result\.data\.\*\.BackupDescription\.SourceTableDetails\.TableSizeBytes | numeric |  |  
action\_result\.data\.\*\.BackupDescription\.SourceTableDetails\.ProvisionedThroughput\.ReadCapacityUnits | numeric |  |   3 
action\_result\.data\.\*\.BackupDescription\.SourceTableDetails\.ProvisionedThroughput\.WriteCapacityUnits | numeric |  |   3 
action\_result\.data\.\*\.BackupDescription\.SourceTableDetails\.TableCreationDateTime | string |  |   2023\-02\-16 10\:13\:02\.238000\+00\:00 
action\_result\.data\.\*\.BackupDescription\.SourceTableFeatureDetails\.SSEDescription\.Status | string |  |   ENABLED 
action\_result\.data\.\*\.BackupDescription\.SourceTableFeatureDetails\.SSEDescription\.SSEType | string |  |   KMS 
action\_result\.data\.\*\.BackupDescription\.SourceTableFeatureDetails\.SSEDescription\.KMSMasterKeyArn | string |  |   arn\:aws\:kms\:us\-east\-1\:157568067690\:key/1651022c\-3833\-4ab4\-a782\-df260339eb0c 
action\_result\.data\.\*\.BackupDescription\.SourceTableFeatureDetails\.StreamDescription\.StreamEnabled | boolean |  |   True  False 
action\_result\.data\.\*\.BackupDescription\.SourceTableFeatureDetails\.StreamDescription\.StreamViewType | string |  |   NEW\_AND\_OLD\_IMAGES 
action\_result\.data\.\*\.BackupDescription\.SourceTableFeatureDetails\.LocalSecondaryIndexes\.\*\.IndexName | string |  |   lsi\_sort1\-index 
action\_result\.data\.\*\.BackupDescription\.SourceTableFeatureDetails\.LocalSecondaryIndexes\.\*\.KeySchema\.\*\.KeyType | string |  |   HASH 
action\_result\.data\.\*\.BackupDescription\.SourceTableFeatureDetails\.LocalSecondaryIndexes\.\*\.KeySchema\.\*\.AttributeName | string |  |   test\_part\_key 
action\_result\.data\.\*\.BackupDescription\.SourceTableFeatureDetails\.LocalSecondaryIndexes\.\*\.Projection\.ProjectionType | string |  |   INCLUDE 
action\_result\.data\.\*\.BackupDescription\.SourceTableFeatureDetails\.GlobalSecondaryIndexes\.\*\.IndexName | string |  |   gsi\_part1\-gsi\_sort1\-index 
action\_result\.data\.\*\.BackupDescription\.SourceTableFeatureDetails\.GlobalSecondaryIndexes\.\*\.KeySchema\.\*\.KeyType | string |  |   HASH 
action\_result\.data\.\*\.BackupDescription\.SourceTableFeatureDetails\.GlobalSecondaryIndexes\.\*\.KeySchema\.\*\.AttributeName | string |  |   gsi\_part1 
action\_result\.data\.\*\.BackupDescription\.SourceTableFeatureDetails\.GlobalSecondaryIndexes\.\*\.Projection\.ProjectionType | string |  |   INCLUDE 
action\_result\.data\.\*\.BackupDescription\.SourceTableFeatureDetails\.GlobalSecondaryIndexes\.\*\.ProvisionedThroughput\.ReadCapacityUnits | numeric |  |   3 
action\_result\.data\.\*\.BackupDescription\.SourceTableFeatureDetails\.GlobalSecondaryIndexes\.\*\.ProvisionedThroughput\.WriteCapacityUnits | numeric |  |   3 
action\_result\.message | string |  |   Created global table successfully 
action\_result\.summary | string |  |  
summary\.total\_objects | numeric |  |   1 
summary\.total\_objects\_successful | numeric |  |   1   

## action: 'describe table'
Fetch metadata of a table

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**table\_name** |  required  | Name of Table | string |  `aws dynamodb table name` 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action\_result\.status | string |  |   success  failed 
action\_result\.parameter\.table\_name | string |  `aws dynamodb table name`  |   room 
action\_result\.parameter\.credentials | string |  `aws credentials`  |   \{'AccessKeyId'\: 'ASIASJL6ZZZZZ3M7QC2J', 'Expiration'\: '2021\-06\-07 22\:28\:04', 'SecretAccessKey'\: 'ZZZZZAmvLPictcVBPvjJx0d7MRezOuxiLCMZZZZZ', 'SessionToken'\: 'ZZZZZXIvYXdzEN///////////wEaDFRU0s4AVrw0k0oYICK4ATAzOqzAkg9bHY29lYmP59UvVOHjLufOy4s7SnAzOxGqGIXnukLis4TWNhrJl5R5nYyimrm6K/9d0Cw2SW9gO0ZRjEJHWJ\+yY5Qk2QpWctS2BGn4n\+G8cD6zEweCCMj\+ScI5p8n7YI4wOdvXvOsVMmjV6F09Ujqr1w\+NwoKXlglznXGs/7Q1kNZOMiioEhGUyoiHbQb37GCKslDK\+oqe0KNaUKQ96YCepaLgMbMquDgdAM8I0TTxUO0o5ILF/gUyLT04R7QlOfktkdh6Qt0atTS\+xeKi1hirKRizpJ8jjnxGQIikPRToL2v3ZZZZZZ=='\}  # pragma: allowlist secret
action\_result\.data\.\*\.Table | string |  |  
action\_result\.data\.\*\.Table\.TableName | string |  |  
action\_result\.data\.\*\.Table\.TableId | string |  |   44b4bcbc\-b591\-466f\-a05d\-370d7df1561b 
action\_result\.data\.\*\.Table\.TableArn | string |  |   arn\:aws\:dynamodb\:us\-east\-1\:157568067690\:table/test\_playbook\_backup 
action\_result\.data\.\*\.Table\.ItemCount | numeric |  |  
action\_result\.data\.\*\.Table\.KeySchema\.\*\.KeyType | string |  |   HASH 
action\_result\.data\.\*\.Table\.KeySchema\.\*\.AttributeName | string |  |   test\_part\_key 
action\_result\.data\.\*\.Table\.TableStatus | string |  |   ACTIVE 
action\_result\.data\.\*\.Table\.SSEDescription\.Status | string |  |   ENABLED 
action\_result\.data\.\*\.Table\.SSEDescription\.SSEType | string |  |   KMS 
action\_result\.data\.\*\.Table\.SSEDescription\.KMSMasterKeyArn | string |  |   arn\:aws\:kms\:us\-east\-1\:157568067690\:key/mrk\-82136a96ac4241b2afbe568dfe5d11d6 
action\_result\.data\.\*\.Table\.TableSizeBytes | numeric |  |  
action\_result\.data\.\*\.Table\.CreationDateTime | string |  |   2023\-02\-16 10\:15\:15\.823000\+00\:00 
action\_result\.data\.\*\.Table\.AttributeDefinitions\.\*\.AttributeName | string |  |   gsi\_part1 
action\_result\.data\.\*\.Table\.AttributeDefinitions\.\*\.AttributeType | string |  |   N 
action\_result\.data\.\*\.Table\.LocalSecondaryIndexes\.\*\.IndexArn | string |  |   arn\:aws\:dynamodb\:us\-east\-1\:157568067690\:table/test\_playbook\_backup/index/lsi\_sort1\-index 
action\_result\.data\.\*\.Table\.LocalSecondaryIndexes\.\*\.IndexName | string |  |   lsi\_sort1\-index 
action\_result\.data\.\*\.Table\.LocalSecondaryIndexes\.\*\.ItemCount | numeric |  |  
action\_result\.data\.\*\.Table\.LocalSecondaryIndexes\.\*\.KeySchema\.\*\.KeyType | string |  |   HASH 
action\_result\.data\.\*\.Table\.LocalSecondaryIndexes\.\*\.KeySchema\.\*\.AttributeName | string |  |   test\_part\_key 
action\_result\.data\.\*\.Table\.LocalSecondaryIndexes\.\*\.Projection\.ProjectionType | string |  |   INCLUDE 
action\_result\.data\.\*\.Table\.LocalSecondaryIndexes\.\*\.IndexSizeBytes | numeric |  |  
action\_result\.data\.\*\.Table\.ProvisionedThroughput\.ReadCapacityUnits | numeric |  |   3 
action\_result\.data\.\*\.Table\.ProvisionedThroughput\.WriteCapacityUnits | numeric |  |   3 
action\_result\.data\.\*\.Table\.ProvisionedThroughput\.LastDecreaseDateTime | string |  |   2023\-02\-16 10\:17\:58\.707000\+00\:00 
action\_result\.data\.\*\.Table\.ProvisionedThroughput\.NumberOfDecreasesToday | numeric |  |   1 
action\_result\.data\.\*\.Table\.GlobalSecondaryIndexes\.\*\.IndexArn | string |  |   arn\:aws\:dynamodb\:us\-east\-1\:157568067690\:table/test\_playbook\_backup/index/gsi\_part2\-index 
action\_result\.data\.\*\.Table\.GlobalSecondaryIndexes\.\*\.IndexName | string |  |   gsi\_part2\-index 
action\_result\.data\.\*\.Table\.GlobalSecondaryIndexes\.\*\.ItemCount | numeric |  |  
action\_result\.data\.\*\.Table\.GlobalSecondaryIndexes\.\*\.KeySchema\.\*\.KeyType | string |  |   HASH 
action\_result\.data\.\*\.Table\.GlobalSecondaryIndexes\.\*\.KeySchema\.\*\.AttributeName | string |  |   gsi\_part2 
action\_result\.data\.\*\.Table\.GlobalSecondaryIndexes\.\*\.Projection\.ProjectionType | string |  |   ALL 
action\_result\.data\.\*\.Table\.GlobalSecondaryIndexes\.\*\.IndexStatus | string |  |   ACTIVE 
action\_result\.data\.\*\.Table\.GlobalSecondaryIndexes\.\*\.IndexSizeBytes | numeric |  |  
action\_result\.data\.\*\.Table\.GlobalSecondaryIndexes\.\*\.ProvisionedThroughput\.ReadCapacityUnits | numeric |  |   3 
action\_result\.data\.\*\.Table\.GlobalSecondaryIndexes\.\*\.ProvisionedThroughput\.WriteCapacityUnits | numeric |  |   3 
action\_result\.data\.\*\.Table\.GlobalSecondaryIndexes\.\*\.ProvisionedThroughput\.LastDecreaseDateTime | string |  |   2023\-02\-16 10\:18\:06\.128000\+00\:00 
action\_result\.data\.\*\.Table\.GlobalSecondaryIndexes\.\*\.ProvisionedThroughput\.NumberOfDecreasesToday | numeric |  |   1 
action\_result\.data\.\*\.ResponseMetadata\.RequestId | string |  |   IVOH9V6BK0B7Q85I411VMKI4T7VV4KQNSO5AEMVJF66Q9ASUAAJG 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.date | string |  |   Thu, 16 Feb 2023 10\:20\:13 GMT 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.server | string |  |   Server 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.connection | string |  |   keep\-alive 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.x\-amz\-crc32 | string |  |   3323931213 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-type | string |  |   application/x\-amz\-json\-1\.0 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-length | string |  |   2813 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.x\-amzn\-requestid | string |  |   IVOH9V6BK0B7Q85I411VMKI4T7VV4KQNSO5AEMVJF66Q9ASUAAJG 
action\_result\.data\.\*\.ResponseMetadata\.RetryAttempts | numeric |  |  
action\_result\.data\.\*\.ResponseMetadata\.HTTPStatusCode | numeric |  |   200 
action\_result\.data\.\*\.Table\.LatestStreamArn | string |  |   arn\:aws\:dynamodb\:us\-east\-1\:157568067690\:table/test\_playbook/stream/2023\-02\-16T10\:13\:02\.238 
action\_result\.data\.\*\.Table\.LatestStreamLabel | string |  |   2023\-02\-16T10\:13\:02\.238 
action\_result\.data\.\*\.Table\.StreamSpecification\.StreamEnabled | boolean |  |   True  False 
action\_result\.data\.\*\.Table\.StreamSpecification\.StreamViewType | string |  |   NEW\_AND\_OLD\_IMAGES 
action\_result\.message | string |  |   Created global table successfully 
action\_result\.summary | string |  |  
summary\.total\_objects | numeric |  |   1 
summary\.total\_objects\_successful | numeric |  |   1   

## action: 'create global table'
Create a global table from an existing table in the specified region l

Type: **generic**  
Read only: **False**

<ul><li><p>Conditions to create a global table \: </p><ul><li>The table must have the same name as all of the other replicas</li><li>The table must have DynamoDB Streams enabled, with the stream containing both the new and the old images of the item\.</li></ul></li><li><p>If you want to add a new replica table to a global table, each of the following conditions must be true\:</p><ul><li>The table must have the same primary key as all of the other replicas\.</li><li>The table must have the same name as all of the other replicas\.</li><li>The table must have DynamoDB Streams enabled, with the stream containing both the new and the old images of the item\.</li><li>None of the replica tables in the global table can contain any data\.</li></ul></li><li><p>If global secondary indexes are specified, then the following conditions must also be met\:</p><ul><li>The global secondary indexes must have the same name\.</li><li>The global secondary indexes must have the same hash key and sort key \(if present\)\.</li></ul></li><li><p>If local secondary indexes are specified, then the following conditions must also be met\:</p><ul><li>The local secondary indexes must have the same name\.</li><li>The local secondary indexes must have the same hash key and sort key \(if present\)\.</li></ul></li></ul>

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**global\_table\_name** |  required  | Name of Table | string |  `aws dynamodb table name` 
**replication\_group** |  required  | Name of region | string |  `aws region` 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action\_result\.status | string |  |   success  failed 
action\_result\.parameter\.global\_table\_name | string |  `aws dynamodb table name`  |   room 
action\_result\.parameter\.replication\_group | string |  `aws region`  |   us\-east\-1 
action\_result\.parameter\.credentials | string |  `aws credentials`  |   \{'AccessKeyId'\: 'ASIASJL6ZZZZZ3M7QC2J', 'Expiration'\: '2021\-06\-07 22\:28\:04', 'SecretAccessKey'\: 'ZZZZZAmvLPictcVBPvjJx0d7MRezOuxiLCMZZZZZ', 'SessionToken'\: 'ZZZZZXIvYXdzEN///////////wEaDFRU0s4AVrw0k0oYICK4ATAzOqzAkg9bHY29lYmP59UvVOHjLufOy4s7SnAzOxGqGIXnukLis4TWNhrJl5R5nYyimrm6K/9d0Cw2SW9gO0ZRjEJHWJ\+yY5Qk2QpWctS2BGn4n\+G8cD6zEweCCMj\+ScI5p8n7YI4wOdvXvOsVMmjV6F09Ujqr1w\+NwoKXlglznXGs/7Q1kNZOMiioEhGUyoiHbQb37GCKslDK\+oqe0KNaUKQ96YCepaLgMbMquDgdAM8I0TTxUO0o5ILF/gUyLT04R7QlOfktkdh6Qt0atTS\+xeKi1hirKRizpJ8jjnxGQIikPRToL2v3ZZZZZZ=='\}  # pragma: allowlist secret
action\_result\.data | string |  |  
action\_result\.data\.\*\.ResponseMetadata\.RequestId | string |  |   C0FE292C187QISI6FGDGARBR7FVV4KQNSO5AEMVJF66Q9ASUAAJG 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.date | string |  |   Thu, 22 Sep 2022 11\:50\:25 GMT 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.server | string |  |   Server 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.connection | string |  |   keep\-alive 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.x\-amz\-crc32 | string |  |   1081780290 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-type | string |  |   application/x\-amz\-json\-1\.0 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-length | string |  |   236 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.x\-amzn\-requestid | string |  |   C0FE292C187QISI6FGDGARBR7FVV4KQNSO5AEMVJF66Q9ASUAAJG 
action\_result\.data\.\*\.ResponseMetadata\.RetryAttempts | numeric |  |   0 
action\_result\.data\.\*\.ResponseMetadata\.HTTPStatusCode | numeric |  |   200 
action\_result\.data\.\*\.GlobalTableDescription\.GlobalTableArn | string |  |   arn\:aws\:dynamodb\:\:157568067690\:global\-table/room 
action\_result\.data\.\*\.GlobalTableDescription\.GlobalTableName | string |  |   room 
action\_result\.data\.\*\.GlobalTableDescription\.CreationDateTime | string |  |   2022\-09\-22 11\:50\:25\.594000\+00\:00 
action\_result\.data\.\*\.GlobalTableDescription\.ReplicationGroup\.\*\.RegionName | string |  |   us\-east\-1 
action\_result\.data\.\*\.GlobalTableDescription\.GlobalTableStatus | string |  |   CREATING 
action\_result\.message | string |  |   Created global table successfully 
action\_result\.summary | string |  |  
summary\.total\_objects | numeric |  |   1 
summary\.total\_objects\_successful | numeric |  |   1   

## action: 'list global tables'
List all global tables that have a replica in the specified Region

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**exclusive\_start\_global\_table\_name** |  optional  | List global tables after specific given global table name | string |  `aws dynamodb table name` 
**region\_name** |  optional  | List the global tables in a specific Region | string |  `aws region` 
**max\_items** |  optional  | Maximum number of tables to fetch | numeric | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action\_result\.status | string |  |   success  failed 
action\_result\.parameter\.exclusive\_start\_global\_table\_name | string |  `aws dynamodb table name`  |   cars\_backup 
action\_result\.parameter\.region\_name | string |  `aws region`  |   us\-east\-1 
action\_result\.parameter\.max\_items | numeric |  |   3 
action\_result\.parameter\.credentials | string |  `aws credentials`  |   \{'AccessKeyId'\: 'ASIASJL6ZZZZZ3M7QC2J', 'Expiration'\: '2021\-06\-07 22\:28\:04', 'SecretAccessKey'\: 'ZZZZZAmvLPictcVBPvjJx0d7MRezOuxiLCMZZZZZ', 'SessionToken'\: 'ZZZZZXIvYXdzEN///////////wEaDFRU0s4AVrw0k0oYICK4ATAzOqzAkg9bHY29lYmP59UvVOHjLufOy4s7SnAzOxGqGIXnukLis4TWNhrJl5R5nYyimrm6K/9d0Cw2SW9gO0ZRjEJHWJ\+yY5Qk2QpWctS2BGn4n\+G8cD6zEweCCMj\+ScI5p8n7YI4wOdvXvOsVMmjV6F09Ujqr1w\+NwoKXlglznXGs/7Q1kNZOMiioEhGUyoiHbQb37GCKslDK\+oqe0KNaUKQ96YCepaLgMbMquDgdAM8I0TTxUO0o5ILF/gUyLT04R7QlOfktkdh6Qt0atTS\+xeKi1hirKRizpJ8jjnxGQIikPRToL2v3ZZZZZZ=='\}  # pragma: allowlist secret
action\_result\.data\.\*\.GlobalTables\.\*\.GlobalTableName | string |  `aws dynamodb table name`  |   cars 
action\_result\.data\.\*\.GlobalTables\.\*\.ReplicationGroup\.\*\.RegionName | string |  `aws region`  |   us\-east\-2 
action\_result\.data\.\*\.ResponseMetadata\.RequestId | string |  |   RP572T69FGKGL2E8RI23932NPNVV4KQNSO5AEMVJF66Q9ASUAAJG 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.date | string |  |   Thu, 22 Sep 2022 05\:53\:30 GMT 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.server | string |  |   Server 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.connection | string |  |   keep\-alive 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.x\-amz\-crc32 | string |  |   2321728776 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-type | string |  |   application/x\-amz\-json\-1\.0 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-length | string |  |   224 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.x\-amzn\-requestid | string |  |   RP572T69FGKGL2E8RI23932NPNVV4KQNSO5AEMVJF66Q9ASUAAJG 
action\_result\.data\.\*\.ResponseMetadata\.RetryAttempts | numeric |  |   0 
action\_result\.data\.\*\.ResponseMetadata\.HTTPStatusCode | numeric |  |   200 
action\_result\.data\.\*\.LastEvaluatedGlobalTableName | string |  |   fruits 
action\_result\.message | string |  |   Fetched global table list successfully 
action\_result\.summary | string |  |  
summary\.total\_objects | numeric |  |   1 
summary\.total\_objects\_successful | numeric |  |   1   

## action: 'list backups'
List all the backups present in the database

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**backup\_type** |  optional  | Backup type | string |  `aws dynamodb backup type` 
**exclusive\_start\_backup\_arn** |  optional  | List backups after specific given backup arn | string |  `aws dynamodb backup arn` 
**max\_items** |  optional  | Maximum number of backups to fetch | numeric | 
**table\_name** |  optional  | List backups of specific table | string |  `aws dynamodb table name` 
**start\_date** |  optional  | List backups created after provided date\.\(Valid date format allowed\: YYYY/MM/DD | string | 
**end\_date** |  optional  | List backups created before provided data\.\(Valid date format allowed\: YYYY/MM/DD\) | string | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action\_result\.status | string |  |   success  failed 
action\_result\.parameter\.backup\_type | string |  `aws dynamodb backup type`  |   USER 
action\_result\.parameter\.exclusive\_start\_backup\_arn | string |  `aws dynamodb backup arn`  |   arn\:aws\:dynamodb\:us\-east\-1\:157568067690\:table/cars/backup/01663158543903\-413ed1de 
action\_result\.parameter\.max\_items | numeric |  |   2 
action\_result\.parameter\.table\_name | string |  `aws dynamodb table name`  |   cars 
action\_result\.parameter\.start\_date | string |  |   2022\-09\-22 11\:30\:03\.118000\+00\:00 
action\_result\.parameter\.end\_date | string |  |   2022\-09\-22 11\:30\:03\.118000\+00\:00 
action\_result\.parameter\.credentials | string |  `aws credentials`  |   \{'AccessKeyId'\: 'ASIASJL6ZZZZZ3M7QC2J', 'Expiration'\: '2021\-06\-07 22\:28\:04', 'SecretAccessKey'\: 'ZZZZZAmvLPictcVBPvjJx0d7MRezOuxiLCMZZZZZ', 'SessionToken'\: 'ZZZZZXIvYXdzEN///////////wEaDFRU0s4AVrw0k0oYICK4ATAzOqzAkg9bHY29lYmP59UvVOHjLufOy4s7SnAzOxGqGIXnukLis4TWNhrJl5R5nYyimrm6K/9d0Cw2SW9gO0ZRjEJHWJ\+yY5Qk2QpWctS2BGn4n\+G8cD6zEweCCMj\+ScI5p8n7YI4wOdvXvOsVMmjV6F09Ujqr1w\+NwoKXlglznXGs/7Q1kNZOMiioEhGUyoiHbQb37GCKslDK\+oqe0KNaUKQ96YCepaLgMbMquDgdAM8I0TTxUO0o5ILF/gUyLT04R7QlOfktkdh6Qt0atTS\+xeKi1hirKRizpJ8jjnxGQIikPRToL2v3ZZZZZZ=='\}  # pragma: allowlist secret
action\_result\.data\.\*\.BackupSummaries\.\*\.TableId | string |  |   c08213e2\-7a1b\-4c44\-abaa\-bf3a52092232 
action\_result\.data\.\*\.BackupSummaries\.\*\.TableArn | string |  |   arn\:aws\:dynamodb\:us\-east\-1\:157568067690\:table/test\_dev\_table 
action\_result\.data\.\*\.BackupSummaries\.\*\.BackupArn | string |  `aws dynamodb backup arn`  |   arn\:aws\:dynamodb\:us\-east\-1\:157568067690\:table/test\_dev\_table/backup/01659614741851\-9435638e 
action\_result\.data\.\*\.BackupSummaries\.\*\.TableName | string |  `aws dynamodb table name`  |   test\_dev\_table 
action\_result\.data\.\*\.BackupSummaries\.\*\.BackupName | string |  |   newDevTableBackup 
action\_result\.data\.\*\.BackupSummaries\.\*\.BackupType | string |  `aws dynamodb backup type`  |   USER 
action\_result\.data\.\*\.BackupSummaries\.\*\.BackupExpiryDateTime | string |  |   2022\-09\-22 11\:30\:03\.118000\+00\:00 
action\_result\.data\.\*\.BackupSummaries\.\*\.BackupStatus | string |  |   AVAILABLE 
action\_result\.data\.\*\.BackupSummaries\.\*\.BackupSizeBytes | numeric |  |   182 
action\_result\.data\.\*\.BackupSummaries\.\*\.BackupCreationDateTime | string |  |   2022\-08\-04 12\:05\:41\.851000\+00\:00 
action\_result\.data\.\*\.ResponseMetadata\.RequestId | string |  |   AME57LA4RM4QDPVM614J1QTMI3VV4KQNSO5AEMVJF66Q9ASUAAJG  6Q42SMS0AFKKI1K8PR67FNVU87VV4KQNSO5AEMVJF66Q9ASUAAJG 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.date | string |  |   Wed, 14 Sep 2022 12\:24\:04 GMT 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.server | string |  |   Server 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.connection | string |  |   keep\-alive 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.x\-amz\-crc32 | string |  |   4139981727 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-type | string |  |   application/x\-amz\-json\-1\.0 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-length | string |  |   1570 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.x\-amzn\-requestid | string |  |   AME57LA4RM4QDPVM614J1QTMI3VV4KQNSO5AEMVJF66Q9ASUAAJG 
action\_result\.data\.\*\.ResponseMetadata\.RetryAttempts | numeric |  |   0 
action\_result\.data\.\*\.ResponseMetadata\.HTTPStatusCode | numeric |  |   200 
action\_result\.message | string |  |   Fetched list of backups successfully 
action\_result\.summary | string |  |  
summary\.total\_objects | numeric |  |   1 
summary\.total\_objects\_successful | numeric |  |   1   

## action: 'delete backup'
Delete backup of a table

Type: **generic**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**backup\_arn** |  required  | ARN associated with the backup | string |  `aws dynamodb backup arn` 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action\_result\.status | string |  |   success  failed 
action\_result\.parameter\.backup\_arn | string |  `aws dynamodb backup arn`  |   arn\:aws\:dynamodb\:us\-east\-1\:157568067690\:table/test\_dev\_table/backup/01663824550617\-bcee6561 
action\_result\.parameter\.credentials | string |  `aws credentials`  |   \{'AccessKeyId'\: 'ASIASJL6ZZZZZ3M7QC2J', 'Expiration'\: '2021\-06\-07 22\:28\:04', 'SecretAccessKey'\: 'ZZZZZAmvLPictcVBPvjJx0d7MRezOuxiLCMZZZZZ', 'SessionToken'\: 'ZZZZZXIvYXdzEN///////////wEaDFRU0s4AVrw0k0oYICK4ATAzOqzAkg9bHY29lYmP59UvVOHjLufOy4s7SnAzOxGqGIXnukLis4TWNhrJl5R5nYyimrm6K/9d0Cw2SW9gO0ZRjEJHWJ\+yY5Qk2QpWctS2BGn4n\+G8cD6zEweCCMj\+ScI5p8n7YI4wOdvXvOsVMmjV6F09Ujqr1w\+NwoKXlglznXGs/7Q1kNZOMiioEhGUyoiHbQb37GCKslDK\+oqe0KNaUKQ96YCepaLgMbMquDgdAM8I0TTxUO0o5ILF/gUyLT04R7QlOfktkdh6Qt0atTS\+xeKi1hirKRizpJ8jjnxGQIikPRToL2v3ZZZZZZ=='\}  # pragma: allowlist secret
action\_result\.data\.\*\.ResponseMetadata\.RequestId | string |  |   HTKF2F7HA47UIUFP1V5TS6MFJBVV4KQNSO5AEMVJF66Q9ASUAAJG  UNOSU88UQ1G3AOQEJHGVV5IJDBVV4KQNSO5AEMVJF66Q9ASUAAJG 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.date | string |  |   Wed, 14 Sep 2022 12\:29\:44 GMT  Thu, 22 Sep 2022 10\:45\:17 GMT 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.server | string |  |   Server 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.connection | string |  |   keep\-alive 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.x\-amz\-crc32 | string |  |   408729803  2968903155 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-type | string |  |   application/x\-amz\-json\-1\.0 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-length | string |  |   769  810 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.x\-amzn\-requestid | string |  |   HTKF2F7HA47UIUFP1V5TS6MFJBVV4KQNSO5AEMVJF66Q9ASUAAJG  UNOSU88UQ1G3AOQEJHGVV5IJDBVV4KQNSO5AEMVJF66Q9ASUAAJG 
action\_result\.data\.\*\.ResponseMetadata\.RetryAttempts | numeric |  |   0 
action\_result\.data\.\*\.ResponseMetadata\.HTTPStatusCode | numeric |  |   200 
action\_result\.data\.\*\.BackupDescription\.BackupDetails\.BackupArn | string |  `aws dynamodb backup arn`  |   arn\:aws\:dynamodb\:us\-east\-1\:157568067690\:table/cars/backup/01663158543903\-413ed1de  arn\:aws\:dynamodb\:us\-east\-1\:157568067690\:table/test\_dev\_table/backup/01663824550617\-bcee6561 
action\_result\.data\.\*\.BackupDescription\.BackupDetails\.BackupName | string |  |   cars\_backup  newDevTableBackup 
action\_result\.data\.\*\.BackupDescription\.BackupDetails\.BackupExpiryDateTime | string |  |   2022\-09\-22 11\:30\:03\.118000\+00\:00 
action\_result\.data\.\*\.BackupDescription\.BackupDetails\.BackupType | string |  `aws dynamodb backup type`  |   USER 
action\_result\.data\.\*\.BackupDescription\.BackupDetails\.BackupStatus | string |  |   DELETED 
action\_result\.data\.\*\.BackupDescription\.BackupDetails\.BackupSizeBytes | numeric |  |   266  352 
action\_result\.data\.\*\.BackupDescription\.BackupDetails\.BackupCreationDateTime | string |  |   2022\-09\-14 12\:29\:03\.903000\+00\:00  2022\-09\-22 05\:29\:10\.617000\+00\:00 
action\_result\.data\.\*\.BackupDescription\.SourceTableDetails\.TableId | string |  |   0fa008bb\-5e6d\-4287\-949e\-9872a952927f  c08213e2\-7a1b\-4c44\-abaa\-bf3a52092232 
action\_result\.data\.\*\.BackupDescription\.SourceTableDetails\.TableArn | string |  |   arn\:aws\:dynamodb\:us\-east\-1\:157568067690\:table/cars  arn\:aws\:dynamodb\:us\-east\-1\:157568067690\:table/test\_dev\_table 
action\_result\.data\.\*\.BackupDescription\.SourceTableDetails\.ItemCount | numeric |  |   3  4 
action\_result\.data\.\*\.BackupDescription\.SourceTableDetails\.KeySchema\.\*\.KeyType | string |  |   HASH 
action\_result\.data\.\*\.BackupDescription\.SourceTableDetails\.KeySchema\.\*\.AttributeName | string |  `aws dynamodb attribute name`  |   VID 
action\_result\.data\.\*\.BackupDescription\.SourceTableDetails\.TableName | string |  `aws dynamodb table name`  |   cars 
action\_result\.data\.\*\.BackupDescription\.SourceTableDetails\.BillingMode | string |  |   PROVISIONED 
action\_result\.data\.\*\.BackupDescription\.SourceTableDetails\.TableSizeBytes | numeric |  |   266  352 
action\_result\.data\.\*\.BackupDescription\.SourceTableDetails\.ProvisionedThroughput\.ReadCapacityUnits | numeric |  |   1 
action\_result\.data\.\*\.BackupDescription\.SourceTableDetails\.ProvisionedThroughput\.WriteCapacityUnits | numeric |  |   1 
action\_result\.data\.\*\.BackupDescription\.SourceTableDetails\.TableCreationDateTime | string |  |   2022\-08\-05 10\:14\:20\.426000\+00\:00  2022\-07\-29 12\:44\:24\.597000\+00\:00 
action\_result\.data\.\*\.BackupDescription\.SourceTableFeatureDetails\.StreamDescription\.StreamEnabled | boolean |  |   True 
action\_result\.data\.\*\.BackupDescription\.SourceTableFeatureDetails\.StreamDescription\.StreamViewType | string |  |   NEW\_AND\_OLD\_IMAGES 
action\_result\.data\.\*\.BackupDescription\.SourceTableFeatureDetails\.SSEDescription\.Status | string |  |   ENABLED 
action\_result\.data\.\*\.BackupDescription\.SourceTableFeatureDetails\.SSEDescription\.SSEType | string |  |   KMS 
action\_result\.data\.\*\.BackupDescription\.SourceTableFeatureDetails\.SSEDescription\.KMSMasterKeyArn | string |  |   arn\:aws\:kms\:us\-east\-1\:157568067690\:key/1651022c\-3833\-4ab4\-a782\-df260339eb0c 
action\_result\.data\.\*\.BackupDescription\.SourceTableFeatureDetails\.LocalSecondaryIndexes\.\*\.IndexName | string |  |   lsi\_sort1\-index 
action\_result\.data\.\*\.BackupDescription\.SourceTableFeatureDetails\.LocalSecondaryIndexes\.\*\.KeySchema\.\*\.KeyType | string |  |   HASH 
action\_result\.data\.\*\.BackupDescription\.SourceTableFeatureDetails\.LocalSecondaryIndexes\.\*\.KeySchema\.\*\.AttributeName | string |  |   test\_part\_key 
action\_result\.data\.\*\.BackupDescription\.SourceTableFeatureDetails\.LocalSecondaryIndexes\.\*\.Projection\.ProjectionType | string |  |   INCLUDE 
action\_result\.data\.\*\.BackupDescription\.SourceTableFeatureDetails\.GlobalSecondaryIndexes\.\*\.IndexName | string |  |   gsi\_part1\-gsi\_sort1\-index 
action\_result\.data\.\*\.BackupDescription\.SourceTableFeatureDetails\.GlobalSecondaryIndexes\.\*\.KeySchema\.\*\.KeyType | string |  |   HASH 
action\_result\.data\.\*\.BackupDescription\.SourceTableFeatureDetails\.GlobalSecondaryIndexes\.\*\.KeySchema\.\*\.AttributeName | string |  |   gsi\_part1 
action\_result\.data\.\*\.BackupDescription\.SourceTableFeatureDetails\.GlobalSecondaryIndexes\.\*\.Projection\.ProjectionType | string |  |   INCLUDE 
action\_result\.data\.\*\.BackupDescription\.SourceTableFeatureDetails\.GlobalSecondaryIndexes\.\*\.ProvisionedThroughput\.ReadCapacityUnits | numeric |  |   3 
action\_result\.data\.\*\.BackupDescription\.SourceTableFeatureDetails\.GlobalSecondaryIndexes\.\*\.ProvisionedThroughput\.WriteCapacityUnits | numeric |  |   3 
action\_result\.message | string |  |   Deleted backup successfully 
action\_result\.summary | string |  |  
summary\.total\_objects | numeric |  |   1 
summary\.total\_objects\_successful | numeric |  |   1   

## action: 'create backup'
Create a backup of an existing table

Type: **generic**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**table\_name** |  required  | Name of the Table to backup | string |  `aws dynamodb table name` 
**backup\_name** |  required  | Name of the backup | string | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action\_result\.status | string |  |   success  failed 
action\_result\.parameter\.table\_name | string |  `aws dynamodb table name`  |   newtable123 
action\_result\.parameter\.backup\_name | string |  |   newtable123\-backup 
action\_result\.parameter\.credentials | string |  `aws credentials`  |   \{'AccessKeyId'\: 'ASIASJL6ZZZZZ3M7QC2J', 'Expiration'\: '2021\-06\-07 22\:28\:04', 'SecretAccessKey'\: 'ZZZZZAmvLPictcVBPvjJx0d7MRezOuxiLCMZZZZZ', 'SessionToken'\: 'ZZZZZXIvYXdzEN///////////wEaDFRU0s4AVrw0k0oYICK4ATAzOqzAkg9bHY29lYmP59UvVOHjLufOy4s7SnAzOxGqGIXnukLis4TWNhrJl5R5nYyimrm6K/9d0Cw2SW9gO0ZRjEJHWJ\+yY5Qk2QpWctS2BGn4n\+G8cD6zEweCCMj\+ScI5p8n7YI4wOdvXvOsVMmjV6F09Ujqr1w\+NwoKXlglznXGs/7Q1kNZOMiioEhGUyoiHbQb37GCKslDK\+oqe0KNaUKQ96YCepaLgMbMquDgdAM8I0TTxUO0o5ILF/gUyLT04R7QlOfktkdh6Qt0atTS\+xeKi1hirKRizpJ8jjnxGQIikPRToL2v3ZZZZZZ=='\}  # pragma: allowlist secret
action\_result\.data\.\*\.BackupDetails\.BackupArn | string |  `aws dynamodb backup arn`  |   arn\:aws\:dynamodb\:us\-east\-1\:157568067690\:table/cars/backup/01663158543903\-413ed1de 
action\_result\.data\.\*\.BackupDetails\.BackupName | string |  |   cars\_backup 
action\_result\.data\.\*\.BackupDetails\.BackupType | string |  `aws dynamodb backup type`  |   USER 
action\_result\.data\.\*\.BackupDetails\.BackupStatus | string |  |   CREATING 
action\_result\.data\.\*\.BackupDetails\.BackupSizeBytes | numeric |  |   266  0 
action\_result\.data\.\*\.BackupDetails\.BackupCreationDateTime | string |  |   2022\-09\-14 12\:29\:03\.903000\+00\:00 
action\_result\.data\.\*\.BackupDetails\.BackupExpiryDateTime | string |  |   2022\-09\-22 11\:30\:03\.118000\+00\:00 
action\_result\.data\.\*\.ResponseMetadata\.RequestId | string |  |   K109PP9CK2RGFK6BV1HDE87C5JVV4KQNSO5AEMVJF66Q9ASUAAJG 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.date | string |  |   Wed, 14 Sep 2022 12\:29\:03 GMT 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.server | string |  |   Server 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.connection | string |  |   keep\-alive 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.x\-amz\-crc32 | string |  |   1789868498 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-type | string |  |   application/x\-amz\-json\-1\.0 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-length | string |  |   252  264 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.x\-amzn\-requestid | string |  |   K109PP9CK2RGFK6BV1HDE87C5JVV4KQNSO5AEMVJF66Q9ASUAAJG  DPPQT09D3JLAT4VSO7T5CBA3QNVV4KQNSO5AEMVJF66Q9ASUAAJG 
action\_result\.data\.\*\.ResponseMetadata\.RetryAttempts | numeric |  |   0 
action\_result\.data\.\*\.ResponseMetadata\.HTTPStatusCode | numeric |  |   200 
action\_result\.message | string |  |   Created backup successfully 
action\_result\.summary | string |  |  
summary\.total\_objects | numeric |  |   1 
summary\.total\_objects\_successful | numeric |  |   1   

## action: 'restore backup table'
Create a new table from an existing backup

Type: **generic**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**table\_name** |  required  | Name of the table to restore | string |  `aws dynamodb table name` 
**backup\_arn** |  required  | Amazon Resource Name \(ARN\) associated with the backup | string |  `aws dynamodb backup arn` 
**billing\_mode\_override** |  optional  | Billing mode of the restored table | string |  `aws dynamodb billing mode` 
**read\_capacity\_override** |  optional  | Read capacity override \(for PROVISIONED billing mode\) | numeric |  `aws dynamodb read capacity` 
**write\_capacity\_override** |  optional  | Write capacity override \(for PROVISIONED billing mode\) | numeric |  `aws dynamodb write capacity` 
**restore\_secondary\_indexes** |  required  | Restore secondary indexes | string | 
**sse\_enable\_override** |  optional  | Server\-side encryption\(SSE\) setting | string | 
**kms\_master\_key\_id** |  optional  | Key to use for the AWS KMS encryption \(Used when SSE is enabled\) | string |  `aws dynamodb kms master key id` 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action\_result\.status | string |  |   success  failed 
action\_result\.parameter\.table\_name | string |  `aws dynamodb table name`  |   retorenewtable123 
action\_result\.parameter\.backup\_arn | string |  `aws dynamodb backup arn`  |   arn\:aws\:dynamodb\:us\-east\-1\:157568067690\:table/newtable123/backup/01663846203118\-f405802d 
action\_result\.parameter\.billing\_mode\_override | string |  `aws dynamodb billing mode`  |   PROVISIONED 
action\_result\.parameter\.read\_capacity\_override | numeric |  `aws dynamodb read capacity`  |  
action\_result\.parameter\.write\_capacity\_override | numeric |  `aws dynamodb write capacity`  |  
action\_result\.parameter\.restore\_secondary\_indexes | string |  |   Restore the entire table 
action\_result\.parameter\.sse\_enable\_override | string |  |   True 
action\_result\.parameter\.kms\_master\_key\_id | string |  `aws dynamodb kms master key id`  |   arn\:aws\:kms\:us\-east\-1\:157568067690\:key/1651022c\-3833\-4ab4\-a782\-df260339eb0c 
action\_result\.parameter\.credentials | string |  `aws credentials`  |   \{'AccessKeyId'\: 'ASIASJL6ZZZZZ3M7QC2J', 'Expiration'\: '2021\-06\-07 22\:28\:04', 'SecretAccessKey'\: 'ZZZZZAmvLPictcVBPvjJx0d7MRezOuxiLCMZZZZZ', 'SessionToken'\: 'ZZZZZXIvYXdzEN///////////wEaDFRU0s4AVrw0k0oYICK4ATAzOqzAkg9bHY29lYmP59UvVOHjLufOy4s7SnAzOxGqGIXnukLis4TWNhrJl5R5nYyimrm6K/9d0Cw2SW9gO0ZRjEJHWJ\+yY5Qk2QpWctS2BGn4n\+G8cD6zEweCCMj\+ScI5p8n7YI4wOdvXvOsVMmjV6F09Ujqr1w\+NwoKXlglznXGs/7Q1kNZOMiioEhGUyoiHbQb37GCKslDK\+oqe0KNaUKQ96YCepaLgMbMquDgdAM8I0TTxUO0o5ILF/gUyLT04R7QlOfktkdh6Qt0atTS\+xeKi1hirKRizpJ8jjnxGQIikPRToL2v3ZZZZZZ=='\}  # pragma: allowlist secret
action\_result\.data | string |  |  
action\_result\.data\.\*\.ResponseMetadata\.RequestId | string |  |   D1PGDOFSG8MPUAOL4TM2NN7TR7VV4KQNSO5AEMVJF66Q9ASUAAJG 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.date | string |  |   Thu, 22 Sep 2022 11\:43\:36 GMT 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.server | string |  |   Server 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.connection | string |  |   keep\-alive 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.x\-amz\-crc32 | string |  |   4165026467 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-type | string |  |   application/x\-amz\-json\-1\.0 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-length | string |  |   1995 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.x\-amzn\-requestid | string |  |   D1PGDOFSG8MPUAOL4TM2NN7TR7VV4KQNSO5AEMVJF66Q9ASUAAJG 
action\_result\.data\.\*\.ResponseMetadata\.RetryAttempts | numeric |  |   0 
action\_result\.data\.\*\.ResponseMetadata\.HTTPStatusCode | numeric |  |   200 
action\_result\.data\.\*\.TableDescription\.TableId | string |  |   67ede490\-028f\-40ca\-b286\-2e320f2295c4 
action\_result\.data\.\*\.TableDescription\.TableArn | string |  |   arn\:aws\:dynamodb\:us\-east\-1\:157568067690\:table/retorenewtable123 
action\_result\.data\.\*\.TableDescription\.ItemCount | numeric |  |   0 
action\_result\.data\.\*\.TableDescription\.KeySchema\.\*\.KeyType | string |  |   HASH 
action\_result\.data\.\*\.TableDescription\.KeySchema\.\*\.AttributeName | string |  `aws dynamodb attribute name`  |   ID 
action\_result\.data\.\*\.TableDescription\.TableName | string |  `aws dynamodb table name`  |   retorenewtable123 
action\_result\.data\.\*\.TableDescription\.TableStatus | string |  |   CREATING 
action\_result\.data\.\*\.TableDescription\.RestoreSummary\.SourceTableArn | string |  |   arn\:aws\:dynamodb\:us\-east\-1\:157568067690\:table/newtable123 
action\_result\.data\.\*\.TableDescription\.RestoreSummary\.RestoreDateTime | string |  |   2022\-09\-22 11\:30\:03\.118000\+00\:00 
action\_result\.data\.\*\.TableDescription\.RestoreSummary\.SourceBackupArn | string |  `aws dynamodb backup arn`  |   arn\:aws\:dynamodb\:us\-east\-1\:157568067690\:table/newtable123/backup/01663846203118\-f405802d 
action\_result\.data\.\*\.TableDescription\.RestoreSummary\.RestoreInProgress | boolean |  |   True 
action\_result\.data\.\*\.TableDescription\.SSEDescription\.Status | string |  |   ENABLED 
action\_result\.data\.\*\.TableDescription\.SSEDescription\.SSEType | string |  |   KMS 
action\_result\.data\.\*\.TableDescription\.SSEDescription\.KMSMasterKeyArn | string |  `aws dynamodb kms master key id`  |   arn\:aws\:kms\:us\-east\-1\:157568067690\:key/1651022c\-3833\-4ab4\-a782\-df260339eb0c 
action\_result\.data\.\*\.TableDescription\.TableSizeBytes | numeric |  |   0 
action\_result\.data\.\*\.TableDescription\.CreationDateTime | string |  |   2022\-09\-22 11\:43\:36\.491000\+00\:00 
action\_result\.data\.\*\.TableDescription\.BillingModeSummary\.BillingMode | string |  |   PROVISIONED 
action\_result\.data\.\*\.TableDescription\.AttributeDefinitions\.\*\.AttributeName | string |  `aws dynamodb attribute name`  |   newname 
action\_result\.data\.\*\.TableDescription\.AttributeDefinitions\.\*\.AttributeType | string |  `aws dynamodb attribute datatype`  |   S 
action\_result\.data\.\*\.TableDescription\.LocalSecondaryIndexes\.\*\.IndexArn | string |  |   arn\:aws\:dynamodb\:us\-east\-1\:157568067690\:table/retorenewtable123/index/testdatast\-index 
action\_result\.data\.\*\.TableDescription\.LocalSecondaryIndexes\.\*\.IndexName | string |  |   testdatast\-index 
action\_result\.data\.\*\.TableDescription\.LocalSecondaryIndexes\.\*\.ItemCount | numeric |  |   0 
action\_result\.data\.\*\.TableDescription\.LocalSecondaryIndexes\.\*\.KeySchema\.\*\.KeyType | string |  |   HASH 
action\_result\.data\.\*\.TableDescription\.LocalSecondaryIndexes\.\*\.KeySchema\.\*\.AttributeName | string |  `aws dynamodb attribute name`  |   ID 
action\_result\.data\.\*\.TableDescription\.LocalSecondaryIndexes\.\*\.Projection\.ProjectionType | string |  |   ALL 
action\_result\.data\.\*\.TableDescription\.LocalSecondaryIndexes\.\*\.IndexSizeBytes | numeric |  |   0 
action\_result\.data\.\*\.TableDescription\.ProvisionedThroughput\.ReadCapacityUnits | numeric |  `aws dynamodb read capacity`  |   4 
action\_result\.data\.\*\.TableDescription\.ProvisionedThroughput\.WriteCapacityUnits | numeric |  `aws dynamodb write capacity`  |   4 
action\_result\.data\.\*\.TableDescription\.ProvisionedThroughput\.NumberOfDecreasesToday | numeric |  |   0 
action\_result\.data\.\*\.TableDescription\.GlobalSecondaryIndexes\.\*\.IndexArn | string |  |   arn\:aws\:dynamodb\:us\-east\-1\:157568067690\:table/retorenewtable123/index/newid\-newname\-index 
action\_result\.data\.\*\.TableDescription\.GlobalSecondaryIndexes\.\*\.IndexName | string |  |   newid\-newname\-index 
action\_result\.data\.\*\.TableDescription\.GlobalSecondaryIndexes\.\*\.ItemCount | numeric |  |   0 
action\_result\.data\.\*\.TableDescription\.GlobalSecondaryIndexes\.\*\.KeySchema\.\*\.KeyType | string |  |   HASH 
action\_result\.data\.\*\.TableDescription\.GlobalSecondaryIndexes\.\*\.KeySchema\.\*\.AttributeName | string |  `aws dynamodb attribute name`  |   newid 
action\_result\.data\.\*\.TableDescription\.GlobalSecondaryIndexes\.\*\.Projection\.ProjectionType | string |  |   INCLUDE 
action\_result\.data\.\*\.TableDescription\.GlobalSecondaryIndexes\.\*\.Projection\.NonKeyAttributes | string |  `aws dynamodb attribute name`  |   num1 
action\_result\.data\.\*\.TableDescription\.GlobalSecondaryIndexes\.\*\.IndexSizeBytes | numeric |  |   0 
action\_result\.data\.\*\.TableDescription\.GlobalSecondaryIndexes\.\*\.ProvisionedThroughput\.ReadCapacityUnits | numeric |  `aws dynamodb read capacity`  |   4 
action\_result\.data\.\*\.TableDescription\.GlobalSecondaryIndexes\.\*\.ProvisionedThroughput\.WriteCapacityUnits | numeric |  `aws dynamodb write capacity`  |   4 
action\_result\.data\.\*\.TableDescription\.GlobalSecondaryIndexes\.\*\.ProvisionedThroughput\.NumberOfDecreasesToday | numeric |  |   0 
action\_result\.message | string |  |   Restored table from backup successfully 
action\_result\.summary | string |  |  
summary\.total\_objects | numeric |  |   1 
summary\.total\_objects\_successful | numeric |  |   1   

## action: 'list tables'
List all the tables present in the database

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**max\_items** |  optional  | Maximum number of tables to fetch | numeric | 
**exclusive\_start\_table\_name** |  optional  | List table after specific given table name | string |  `aws dynamodb table name` 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action\_result\.status | string |  |   success  failed 
action\_result\.parameter\.max\_items | numeric |  |   5 
action\_result\.parameter\.exclusive\_start\_table\_name | string |  `aws dynamodb table name`  |   cars2 
action\_result\.parameter\.credentials | string |  `aws credentials`  |   \{'AccessKeyId'\: 'ASIASJL6ZZZZZ3M7QC2J', 'Expiration'\: '2021\-06\-07 22\:28\:04', 'SecretAccessKey'\: 'ZZZZZAmvLPictcVBPvjJx0d7MRezOuxiLCMZZZZZ', 'SessionToken'\: 'ZZZZZXIvYXdzEN///////////wEaDFRU0s4AVrw0k0oYICK4ATAzOqzAkg9bHY29lYmP59UvVOHjLufOy4s7SnAzOxGqGIXnukLis4TWNhrJl5R5nYyimrm6K/9d0Cw2SW9gO0ZRjEJHWJ\+yY5Qk2QpWctS2BGn4n\+G8cD6zEweCCMj\+ScI5p8n7YI4wOdvXvOsVMmjV6F09Ujqr1w\+NwoKXlglznXGs/7Q1kNZOMiioEhGUyoiHbQb37GCKslDK\+oqe0KNaUKQ96YCepaLgMbMquDgdAM8I0TTxUO0o5ILF/gUyLT04R7QlOfktkdh6Qt0atTS\+xeKi1hirKRizpJ8jjnxGQIikPRToL2v3ZZZZZZ=='\}  # pragma: allowlist secret
action\_result\.data | string |  |  
action\_result\.data\.\*\.TableNames | string |  `aws dynamodb table name`  |   room\_test\_1 
action\_result\.message | string |  |   Fetched list of table successfully 
action\_result\.summary | string |  |  
summary\.total\_objects | numeric |  |   1 
summary\.total\_objects\_successful | numeric |  |   1   

## action: 'delete table'
Delete a table from the database

Type: **generic**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**table\_name** |  required  | Name of Table to delete | string |  `aws dynamodb table name` 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action\_result\.status | string |  |   success  failed 
action\_result\.parameter\.table\_name | string |  `aws dynamodb table name`  |   testdata 
action\_result\.parameter\.credentials | string |  `aws credentials`  |   \{'AccessKeyId'\: 'ASIASJL6ZZZZZ3M7QC2J', 'Expiration'\: '2021\-06\-07 22\:28\:04', 'SecretAccessKey'\: 'ZZZZZAmvLPictcVBPvjJx0d7MRezOuxiLCMZZZZZ', 'SessionToken'\: 'ZZZZZXIvYXdzEN///////////wEaDFRU0s4AVrw0k0oYICK4ATAzOqzAkg9bHY29lYmP59UvVOHjLufOy4s7SnAzOxGqGIXnukLis4TWNhrJl5R5nYyimrm6K/9d0Cw2SW9gO0ZRjEJHWJ\+yY5Qk2QpWctS2BGn4n\+G8cD6zEweCCMj\+ScI5p8n7YI4wOdvXvOsVMmjV6F09Ujqr1w\+NwoKXlglznXGs/7Q1kNZOMiioEhGUyoiHbQb37GCKslDK\+oqe0KNaUKQ96YCepaLgMbMquDgdAM8I0TTxUO0o5ILF/gUyLT04R7QlOfktkdh6Qt0atTS\+xeKi1hirKRizpJ8jjnxGQIikPRToL2v3ZZZZZZ=='\}  # pragma: allowlist secret
action\_result\.data\.\*\.TableNames | string |  |  
action\_result\.data\.\*\.ResponseMetadata\.RequestId | string |  |   KMO2UQHBJ1L4DL15K1RN4HVGD7VV4KQNSO5AEMVJF66Q9ASUAAJG 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.date | string |  |   Wed, 21 Sep 2022 18\:29\:19 GMT 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.server | string |  |   Server 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.connection | string |  |   keep\-alive 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.x\-amz\-crc32 | string |  |   3710880937 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-type | string |  |   application/x\-amz\-json\-1\.0 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-length | string |  |   310 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.x\-amzn\-requestid | string |  |   KMO2UQHBJ1L4DL15K1RN4HVGD7VV4KQNSO5AEMVJF66Q9ASUAAJG 
action\_result\.data\.\*\.ResponseMetadata\.RetryAttempts | numeric |  |   0 
action\_result\.data\.\*\.ResponseMetadata\.HTTPStatusCode | numeric |  |   200 
action\_result\.data\.\*\.TableDescription\.TableId | string |  |   78197d82\-7d17\-49ad\-b622\-fb5a619832dd 
action\_result\.data\.\*\.TableDescription\.TableArn | string |  |   arn\:aws\:dynamodb\:us\-east\-1\:157568067690\:table/testdata 
action\_result\.data\.\*\.TableDescription\.ItemCount | numeric |  |   0 
action\_result\.data\.\*\.TableDescription\.TableName | string |  |   testdata 
action\_result\.data\.\*\.TableDescription\.TableStatus | string |  |   DELETING 
action\_result\.data\.\*\.TableDescription\.TableSizeBytes | numeric |  |   0 
action\_result\.data\.\*\.TableDescription\.ProvisionedThroughput\.ReadCapacityUnits | numeric |  |   5 
action\_result\.data\.\*\.TableDescription\.ProvisionedThroughput\.WriteCapacityUnits | numeric |  |   5 
action\_result\.data\.\*\.TableDescription\.ProvisionedThroughput\.NumberOfDecreasesToday | numeric |  |   0 
action\_result\.data\.\*\.TableDescription\.SSEDescription\.Status | string |  |   ENABLED 
action\_result\.data\.\*\.TableDescription\.SSEDescription\.SSEType | string |  |   KMS 
action\_result\.data\.\*\.TableDescription\.SSEDescription\.KMSMasterKeyArn | string |  |   arn\:aws\:kms\:us\-east\-1\:157568067690\:key/1651022c\-3833\-4ab4\-a782\-df260339eb0c 
action\_result\.data\.\*\.TableDescription\.LatestStreamArn | string |  |   arn\:aws\:dynamodb\:us\-east\-1\:157568067690\:table/test\_playbook/stream/2023\-02\-16T10\:13\:02\.238 
action\_result\.data\.\*\.TableDescription\.LatestStreamLabel | string |  |   2023\-02\-16T10\:13\:02\.238 
action\_result\.data\.\*\.TableDescription\.StreamSpecification\.StreamEnabled | boolean |  |   True  False 
action\_result\.data\.\*\.TableDescription\.StreamSpecification\.StreamViewType | string |  |   NEW\_AND\_OLD\_IMAGES 
action\_result\.message | string |  |   Deleted Table Successfully 
action\_result\.summary | string |  |  
summary\.total\_objects | numeric |  |   1 
summary\.total\_objects\_successful | numeric |  |   1   

## action: 'create table'
Create a table in the database

Type: **generic**  
Read only: **False**

<ul><li> Each table has a Primary Key to identify items uniquely\. The primary in DynamoDB is made up of Partition Key and Sort Key\. Sort is Optional, but once the table is created you cannot add/update Sort Key </li><li><p>All the keys\(partition & sort\) in Dynamodb have only three supported datatype \[String,Number,Binary\]</p></li><li><div><p>The Billing mode defines how you going to be charged for read and write throughput and how you manage capacity\.This setting can be changed later\.</p><p>Billing Mode has two values, by default it will be set to <strong>PROVISIONED</strong>\.</p><ul><li>PROVISIONED\: Sets the billing mode to Provisioned Mode</li><li>PAY PER REQUEST\: Sets the billing mode to On\-Demand Mode</li></ul><p> When the billing mode is Provisioned, read and write capacity becomes required parameters\. The values for read and write capacity units are default set to 5\. Also, auto\-scaling is disabled\. </p></div></li><li><div><p>Secondary Indexes</p><ul><li> For creating Local Secondary Index \(LSI\) and Global Secondary Index \(GSI\), please refer the documentation above\. </li><li> Once created local secondary index cannot be added/updated, but Global Secondary can be created\. </li></ul></li></div></li><li><div><p> A DynamoDB stream is an ordered flow of information about changes to items in a DynamoDB table\. When you enable a stream on a table, DynamoDB captures information about every modification to data items in the table\. To enable streams for table, check the enable stream checkbox\. </p><p>If stream are enabled you need to select stream view type\. There are four options you could select from\: </p><ul><li> KEYS ONLY\: Only the key attributes of the modified item are written to the stream\. </li><li> NEW IMAGE\: The entire item, as it appears after it was modified, is written to the stream\. </li><li> OLD IMAGE\: The entire item, as it appeared before it was modified, is written to the stream\. </li><li> NEW AND OLD IMAGES\: Both the new and the old item images of the item are written to the stream\. </li></ul></div></li><li><div><p>SSE</p><ul><li> Set it to true to use server\-side encryption\. </li><li> For the KMS master key id provide the KMS key value that should be used for encryption\. </li></ul></div></li><li><p> The KMS key that should be used for the KMS encryption\. To specify a key, use its key ID, Amazon Resource Name \(ARN\), alias name, or alias ARN\. Note that you should only provide this parameter if the key is different from the default DynamoDB key alias/aws/dynamodb </p></li><li> To learn the way of taking input for local and global secondary index, please refer the documentation provided above for Local and Global Secondary Index\. </li><li> To add tags to you table, follow the step given below <ul><li> For a single values for tags, pass a JSON object\. The JSON object should contain the 'Key' and 'Value' keys\. These two keys are required and without these adding tags won't be possible\. <pre> \{ 'Key' \: 'key\_data', 'Value' \: 'value\_data' \} </pre></li><li> For multiple values in tags, pass a list of JSON object\. <pre> \[ \{ 'Key' \: 'key\_data1', 'Value' \: 'value\_data1' \}, \{ 'Key' \: 'key\_data2', 'Value' \: 'value\_data2' \} \] </pre></li></ul></li></ul>\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**table\_name** |  required  | Name of table to be created | string |  `aws dynamodb table name` 
**billing\_mode** |  optional  | Billing mode to be used for table | string | 
**partition\_key\_name** |  required  | Partition key name for table items | string |  `aws dynamodb partition key name` 
**partition\_key\_datatype** |  required  | Datatype of partition key | string | 
**sort\_key\_name** |  optional  | Sort key name for table items | string |  `aws dynamodb sort key name` 
**sort\_key\_datatype** |  optional  | Datatype for sort key | string | 
**read\_capacity\_units** |  optional  | Read capacity units for provisioned mode | numeric | 
**write\_capacity\_units** |  optional  | Write capacity units for provisioned mode | numeric | 
**local\_secondary\_index** |  optional  | JSON input for creating local secondary index | string | 
**global\_secondary\_index** |  optional  | JSON input for creating global secondary index | string | 
**enable\_stream** |  optional  | Enable streams for the table | boolean | 
**stream\_view\_type** |  optional  | View type of dynamodb stream | string | 
**sse** |  required  | Settings used to enable server\-side encryption | string | 
**kms\_master\_key\_id** |  optional  | The KMS key that should be used for the KMS encryption | string | 
**tags** |  optional  | List of tags to add to table | string | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action\_result\.status | string |  |   success  failed 
action\_result\.parameter\.table\_name | string |  `aws dynamodb table name`  |   newtable123 
action\_result\.parameter\.billing\_mode | string |  |   PROVISIONED 
action\_result\.parameter\.partition\_key\_name | string |  `aws dynamodb partition key name`  |   ID 
action\_result\.parameter\.sort\_key\_name | string |  `aws dynamodb sort key name`  |   name 
action\_result\.parameter\.partition\_key\_datatype | string |  |   Number 
action\_result\.parameter\.sort\_key\_datatype | string |  |   String 
action\_result\.parameter\.read\_capacity\_units | numeric |  |   4 
action\_result\.parameter\.write\_capacity\_units | numeric |  |   4 
action\_result\.parameter\.local\_secondary\_index | string |  |   \{"attribute\_projection"\: "ALL",
    "sort\_key\_name"\: "testdatast",
    "sort\_key\_datatype"\:  "string"\} 
action\_result\.parameter\.global\_secondary\_index | string |  |   \{
    "attribute\_projection"\: "INCLUDE",
    "partition\_key\_name"\: "newid",
    "partition\_key\_datatype"\: "string",
    "sort\_key\_name"\:  "newname",
    "sort\_key\_datatype"\:  "string",
    "NonKeyAttributes"\:  \["num1","num2"\]
\} 
action\_result\.parameter\.enable\_stream | boolean |  |   True 
action\_result\.parameter\.stream\_view\_type | string |  |   NEW\_IMAGE 
action\_result\.parameter\.sse | string |  |   False 
action\_result\.parameter\.kms\_master\_key\_id | string |  |   arn\:aws\:kms\:us\-east\-1\:157568067690\:key/1651022c\-3833\-4ab4\-a782\-df260339eb0c 
action\_result\.parameter\.tags | string |  |   events 
action\_result\.parameter\.credentials | string |  `aws credentials`  |   \{'AccessKeyId'\: 'ASIASJL6ZZZZZ3M7QC2J', 'Expiration'\: '2021\-06\-07 22\:28\:04', 'SecretAccessKey'\: 'ZZZZZAmvLPictcVBPvjJx0d7MRezOuxiLCMZZZZZ', 'SessionToken'\: 'ZZZZZXIvYXdzEN///////////wEaDFRU0s4AVrw0k0oYICK4ATAzOqzAkg9bHY29lYmP59UvVOHjLufOy4s7SnAzOxGqGIXnukLis4TWNhrJl5R5nYyimrm6K/9d0Cw2SW9gO0ZRjEJHWJ\+yY5Qk2QpWctS2BGn4n\+G8cD6zEweCCMj\+ScI5p8n7YI4wOdvXvOsVMmjV6F09Ujqr1w\+NwoKXlglznXGs/7Q1kNZOMiioEhGUyoiHbQb37GCKslDK\+oqe0KNaUKQ96YCepaLgMbMquDgdAM8I0TTxUO0o5ILF/gUyLT04R7QlOfktkdh6Qt0atTS\+xeKi1hirKRizpJ8jjnxGQIikPRToL2v3ZZZZZZ=='\}  # pragma: allowlist secret
action\_result\.data\.\*\.TableDescription | string |  |  
action\_result\.data\.\*\.ResponseMetadata\.RequestId | string |  |   J0GO5QSIRQPP2O7RAMOAHO1MKVVV4KQNSO5AEMVJF66Q9ASUAAJG 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.date | string |  |   Thu, 22 Sep 2022 06\:07\:34 GMT 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.server | string |  |   Server 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.connection | string |  |   keep\-alive 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.x\-amz\-crc32 | string |  |   2160627733 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-type | string |  |   application/x\-amz\-json\-1\.0 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-length | string |  |   1680 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.x\-amzn\-requestid | string |  |   J0GO5QSIRQPP2O7RAMOAHO1MKVVV4KQNSO5AEMVJF66Q9ASUAAJG 
action\_result\.data\.\*\.ResponseMetadata\.RetryAttempts | numeric |  |   0 
action\_result\.data\.\*\.ResponseMetadata\.HTTPStatusCode | numeric |  |   200 
action\_result\.data\.\*\.TableDescription\.TableId | string |  |   f250b7a4\-20e6\-49cd\-afed\-20de7a883fef 
action\_result\.data\.\*\.TableDescription\.TableArn | string |  |   arn\:aws\:dynamodb\:us\-east\-1\:157568067690\:table/newtable123 
action\_result\.data\.\*\.TableDescription\.ItemCount | numeric |  |   0 
action\_result\.data\.\*\.TableDescription\.KeySchema\.\*\.KeyType | string |  |   HASH 
action\_result\.data\.\*\.TableDescription\.KeySchema\.\*\.AttributeName | string |  |   ID 
action\_result\.data\.\*\.TableDescription\.TableName | string |  |   newtable123 
action\_result\.data\.\*\.TableDescription\.TableStatus | string |  |   CREATING 
action\_result\.data\.\*\.TableDescription\.SSEDescription\.Status | string |  |   ENABLED 
action\_result\.data\.\*\.TableDescription\.SSEDescription\.SSEType | string |  |   KMS 
action\_result\.data\.\*\.TableDescription\.SSEDescription\.KMSMasterKeyArn | string |  |   arn\:aws\:kms\:us\-east\-1\:157568067690\:key/1651022c\-3833\-4ab4\-a782\-df260339eb0c 
action\_result\.data\.\*\.TableDescription\.TableSizeBytes | numeric |  |   0 
action\_result\.data\.\*\.TableDescription\.CreationDateTime | string |  |   2022\-09\-22 06\:07\:34\.858000\+00\:00 
action\_result\.data\.\*\.TableDescription\.AttributeDefinitions\.\*\.AttributeName | string |  |   ID 
action\_result\.data\.\*\.TableDescription\.AttributeDefinitions\.\*\.AttributeType | string |  |   N 
action\_result\.data\.\*\.TableDescription\.LocalSecondaryIndexes\.\*\.IndexArn | string |  |   arn\:aws\:dynamodb\:us\-east\-1\:157568067690\:table/newtable123/index/testdatast\-index 
action\_result\.data\.\*\.TableDescription\.LocalSecondaryIndexes\.\*\.IndexName | string |  |   testdatast\-index 
action\_result\.data\.\*\.TableDescription\.LocalSecondaryIndexes\.\*\.ItemCount | numeric |  |   0 
action\_result\.data\.\*\.TableDescription\.LocalSecondaryIndexes\.\*\.KeySchema\.\*\.KeyType | string |  |   HASH 
action\_result\.data\.\*\.TableDescription\.LocalSecondaryIndexes\.\*\.KeySchema\.\*\.AttributeName | string |  |   ID 
action\_result\.data\.\*\.TableDescription\.LocalSecondaryIndexes\.\*\.Projection\.ProjectionType | string |  |   ALL 
action\_result\.data\.\*\.TableDescription\.LocalSecondaryIndexes\.\*\.IndexSizeBytes | numeric |  |   0 
action\_result\.data\.\*\.TableDescription\.ProvisionedThroughput\.ReadCapacityUnits | numeric |  |   4 
action\_result\.data\.\*\.TableDescription\.ProvisionedThroughput\.WriteCapacityUnits | numeric |  |   4 
action\_result\.data\.\*\.TableDescription\.ProvisionedThroughput\.NumberOfDecreasesToday | numeric |  |   0 
action\_result\.data\.\*\.TableDescription\.GlobalSecondaryIndexes\.\*\.IndexArn | string |  |   arn\:aws\:dynamodb\:us\-east\-1\:157568067690\:table/newtable123/index/newid\-newname\-index 
action\_result\.data\.\*\.TableDescription\.GlobalSecondaryIndexes\.\*\.IndexName | string |  |   newid\-newname\-index 
action\_result\.data\.\*\.TableDescription\.GlobalSecondaryIndexes\.\*\.ItemCount | numeric |  |   0 
action\_result\.data\.\*\.TableDescription\.GlobalSecondaryIndexes\.\*\.KeySchema\.\*\.KeyType | string |  |   HASH 
action\_result\.data\.\*\.TableDescription\.GlobalSecondaryIndexes\.\*\.KeySchema\.\*\.AttributeName | string |  |   newid 
action\_result\.data\.\*\.TableDescription\.GlobalSecondaryIndexes\.\*\.Projection\.ProjectionType | string |  |   INCLUDE 
action\_result\.data\.\*\.TableDescription\.GlobalSecondaryIndexes\.\*\.Projection\.NonKeyAttributes | string |  |   num1 
action\_result\.data\.\*\.TableDescription\.GlobalSecondaryIndexes\.\*\.IndexStatus | string |  |   CREATING 
action\_result\.data\.\*\.TableDescription\.GlobalSecondaryIndexes\.\*\.IndexSizeBytes | numeric |  |   0 
action\_result\.data\.\*\.TableDescription\.GlobalSecondaryIndexes\.\*\.ProvisionedThroughput\.ReadCapacityUnits | numeric |  |   4 
action\_result\.data\.\*\.TableDescription\.GlobalSecondaryIndexes\.\*\.ProvisionedThroughput\.WriteCapacityUnits | numeric |  |   4 
action\_result\.data\.\*\.TableDescription\.GlobalSecondaryIndexes\.\*\.ProvisionedThroughput\.NumberOfDecreasesToday | numeric |  |   0 
action\_result\.data\.\*\.TableDescription\.LatestStreamArn | string |  |   arn\:aws\:dynamodb\:us\-east\-1\:157568067690\:table/test\_playbook/stream/2023\-02\-16T10\:13\:02\.238 
action\_result\.data\.\*\.TableDescription\.LatestStreamLabel | string |  |   2023\-02\-16T10\:13\:02\.238 
action\_result\.data\.\*\.TableDescription\.StreamSpecification\.StreamEnabled | boolean |  |   True  False 
action\_result\.data\.\*\.TableDescription\.StreamSpecification\.StreamViewType | string |  |   NEW\_AND\_OLD\_IMAGES 
action\_result\.message | string |  |   Created Table successfully 
action\_result\.summary | string |  |  
summary\.total\_objects | numeric |  |   1 
summary\.total\_objects\_successful | numeric |  |   1   

## action: 'delete item'
Delete an item from the table

Type: **generic**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**table\_name** |  required  | Table name to delete item from | string |  `aws dynamodb table name` 
**condition\_expression** |  optional  | Condition to be check before delete an item | string | 
**partition\_key\_name** |  required  | Partition key name | string |  `aws dynamodb partition key` 
**sort\_key\_name** |  optional  | Sort key name | string |  `aws dynamodb sort key` 
**partition\_key\_value** |  required  | Partition key value | string | 
**sort\_key\_value** |  optional  | Sort key value | string | 
**partition\_key\_datatype** |  required  | Partition key datatype | string | 
**sort\_key\_datatype** |  optional  | Sort key datatype | string | 
**expression\_attribute\_names** |  optional  | Attribute names json | string | 
**expression\_attribute\_values** |  optional  | Attribute values json | string | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action\_result\.status | string |  |   success  failed 
action\_result\.parameter\.table\_name | string |  `aws dynamodb table name`  |   test\_query 
action\_result\.parameter\.condition\_expression | string |  |  
action\_result\.parameter\.partition\_key\_name | string |  `aws dynamodb partition key`  |   firstname 
action\_result\.parameter\.partition\_key\_value | string |  |   testdata 
action\_result\.parameter\.sort\_key\_name | string |  `aws dynamodb sort key`  |   lastname 
action\_result\.parameter\.sort\_key\_value | string |  |   Kamani 
action\_result\.parameter\.partition\_key\_datatype | string |  |   String 
action\_result\.parameter\.sort\_key\_datatype | string |  |   String 
action\_result\.parameter\.expression\_attribute\_names | string |  |  
action\_result\.parameter\.expression\_attribute\_values | string |  |  
action\_result\.parameter\.credentials | string |  `aws credentials`  |   \{'AccessKeyId'\: 'ASIASJL6ZZZZZ3M7QC2J', 'Expiration'\: '2021\-06\-07 22\:28\:04', 'SecretAccessKey'\: 'ZZZZZAmvLPictcVBPvjJx0d7MRezOuxiLCMZZZZZ', 'SessionToken'\: 'ZZZZZXIvYXdzEN///////////wEaDFRU0s4AVrw0k0oYICK4ATAzOqzAkg9bHY29lYmP59UvVOHjLufOy4s7SnAzOxGqGIXnukLis4TWNhrJl5R5nYyimrm6K/9d0Cw2SW9gO0ZRjEJHWJ\+yY5Qk2QpWctS2BGn4n\+G8cD6zEweCCMj\+ScI5p8n7YI4wOdvXvOsVMmjV6F09Ujqr1w\+NwoKXlglznXGs/7Q1kNZOMiioEhGUyoiHbQb37GCKslDK\+oqe0KNaUKQ96YCepaLgMbMquDgdAM8I0TTxUO0o5ILF/gUyLT04R7QlOfktkdh6Qt0atTS\+xeKi1hirKRizpJ8jjnxGQIikPRToL2v3ZZZZZZ=='\}  # pragma: allowlist secret
action\_result\.data\.\*\.TableNames | string |  |  
action\_result\.data\.\*\.ResponseMetadata\.RequestId | string |  |   91PHHJD3LHOFKAJ7PNM1UF77UBVV4KQNSO5AEMVJF66Q9ASUAAJG 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.date | string |  |   Wed, 21 Sep 2022 18\:17\:41 GMT 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.server | string |  |   Server 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.connection | string |  |   keep\-alive 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.x\-amz\-crc32 | string |  |   2745614147 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-type | string |  |   application/x\-amz\-json\-1\.0 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-length | string |  |   2 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.x\-amzn\-requestid | string |  |   91PHHJD3LHOFKAJ7PNM1UF77UBVV4KQNSO5AEMVJF66Q9ASUAAJG 
action\_result\.data\.\*\.ResponseMetadata\.RetryAttempts | numeric |  |   0 
action\_result\.data\.\*\.ResponseMetadata\.HTTPStatusCode | numeric |  |   200 
action\_result\.message | string |  |   Item deleted successfully 
action\_result\.summary | string |  |  
summary\.total\_objects | numeric |  |   1 
summary\.total\_objects\_successful | numeric |  |   1   

## action: 'put item'
Add an item to the table

Type: **generic**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**table\_name** |  required  | Name of table in which you want to add the item | string |  `aws dynamodb table name` 
**item\_json** |  required  | Item that is to be added in the table | string | 
**condition\_expression** |  optional  | Condition to be checked before inserting an item | string | 
**expression\_attribute\_names** |  optional  | Attribute names json | string | 
**expression\_attribute\_values** |  optional  | Attribute values json | string | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action\_result\.status | string |  |   success  failed 
action\_result\.parameter\.table\_name | string |  `aws dynamodb table name`  |   test\_dev\_table 
action\_result\.parameter\.item\_json | string |  |   \{"testing1"\:\{"S"\:"32"\},"age"\:\{"N"\:"12"\}\} 
action\_result\.parameter\.condition\_expression | string |  |   \#age <> \:age 
action\_result\.parameter\.expression\_attribute\_names | string |  |   \{"\#age"\:"age"\} 
action\_result\.parameter\.expression\_attribute\_values | string |  |   \{"\:age"\:\{"N"\:"12"\}\} 
action\_result\.parameter\.credentials | string |  `aws credentials`  |   \{'AccessKeyId'\: 'ASIASJL6ZZZZZ3M7QC2J', 'Expiration'\: '2021\-06\-07 22\:28\:04', 'SecretAccessKey'\: 'ZZZZZAmvLPictcVBPvjJx0d7MRezOuxiLCMZZZZZ', 'SessionToken'\: 'ZZZZZXIvYXdzEN///////////wEaDFRU0s4AVrw0k0oYICK4ATAzOqzAkg9bHY29lYmP59UvVOHjLufOy4s7SnAzOxGqGIXnukLis4TWNhrJl5R5nYyimrm6K/9d0Cw2SW9gO0ZRjEJHWJ\+yY5Qk2QpWctS2BGn4n\+G8cD6zEweCCMj\+ScI5p8n7YI4wOdvXvOsVMmjV6F09Ujqr1w\+NwoKXlglznXGs/7Q1kNZOMiioEhGUyoiHbQb37GCKslDK\+oqe0KNaUKQ96YCepaLgMbMquDgdAM8I0TTxUO0o5ILF/gUyLT04R7QlOfktkdh6Qt0atTS\+xeKi1hirKRizpJ8jjnxGQIikPRToL2v3ZZZZZZ=='\}  # pragma: allowlist secret
action\_result\.data\.\*\.TableNames | string |  |  
action\_result\.data\.\*\.ResponseMetadata\.RequestId | string |  |   469DQNHNGBMPVBCFVEUIMJQ5FFVV4KQNSO5AEMVJF66Q9ASUAAJG 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.date | string |  |   Thu, 22 Sep 2022 10\:24\:42 GMT 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.server | string |  |   Server 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.connection | string |  |   keep\-alive 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.x\-amz\-crc32 | string |  |   2745614147 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-type | string |  |   application/x\-amz\-json\-1\.0 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-length | string |  |   2 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.x\-amzn\-requestid | string |  |   469DQNHNGBMPVBCFVEUIMJQ5FFVV4KQNSO5AEMVJF66Q9ASUAAJG 
action\_result\.data\.\*\.ResponseMetadata\.RetryAttempts | numeric |  |   0 
action\_result\.data\.\*\.ResponseMetadata\.HTTPStatusCode | numeric |  |   200 
action\_result\.message | string |  |   Item inserted successfully 
action\_result\.summary | string |  |  
summary\.total\_objects | numeric |  |   1 
summary\.total\_objects\_successful | numeric |  |   1   

## action: 'update item'
Update an item in the table

Type: **generic**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**table\_name** |  required  | Name of table in which item is to be updated | string |  `aws dynamodb table name` 
**update\_expression** |  optional  | Expression to update the attribute | string | 
**partition\_key\_name** |  required  | Partition key name | string |  `aws dynamodb partition key` 
**sort\_key\_name** |  optional  | Sort key name | string |  `aws dynamodb sort key` 
**partition\_key\_value** |  required  | Partition key value | string | 
**sort\_key\_value** |  optional  | Sort key value | string | 
**partition\_key\_datatype** |  required  | Partition key datatype | string | 
**sort\_key\_datatype** |  optional  | Sort key datatype | string | 
**expression\_attribute\_names** |  optional  | Attribute names json | string | 
**expression\_attribute\_values** |  optional  | Attribute values json | string | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action\_result\.status | string |  |   success  failed 
action\_result\.parameter\.table\_name | string |  `aws dynamodb table name`  |   test\_dev\_table 
action\_result\.parameter\.partition\_key\_name | string |  `aws dynamodb partition key`  |   testing1 
action\_result\.parameter\.partition\_key\_value | string |  |   2 
action\_result\.parameter\.sort\_key\_name | string |  `aws dynamodb sort key`  |  
action\_result\.parameter\.sort\_key\_value | string |  |  
action\_result\.parameter\.partition\_key\_datatype | string |  |   String 
action\_result\.parameter\.sort\_key\_datatype | string |  |  
action\_result\.parameter\.update\_expression | string |  |   set \#age = \:age 
action\_result\.parameter\.expression\_attribute\_names | string |  |   \{"\#age" \:  "age"\} 
action\_result\.parameter\.expression\_attribute\_values | string |  |   \{"\:age"\:\{"N"\:"24"\}\} 
action\_result\.parameter\.credentials | string |  `aws credentials`  |   \{'AccessKeyId'\: 'ASIASJL6ZZZZZ3M7QC2J', 'Expiration'\: '2021\-06\-07 22\:28\:04', 'SecretAccessKey'\: 'ZZZZZAmvLPictcVBPvjJx0d7MRezOuxiLCMZZZZZ', 'SessionToken'\: 'ZZZZZXIvYXdzEN///////////wEaDFRU0s4AVrw0k0oYICK4ATAzOqzAkg9bHY29lYmP59UvVOHjLufOy4s7SnAzOxGqGIXnukLis4TWNhrJl5R5nYyimrm6K/9d0Cw2SW9gO0ZRjEJHWJ\+yY5Qk2QpWctS2BGn4n\+G8cD6zEweCCMj\+ScI5p8n7YI4wOdvXvOsVMmjV6F09Ujqr1w\+NwoKXlglznXGs/7Q1kNZOMiioEhGUyoiHbQb37GCKslDK\+oqe0KNaUKQ96YCepaLgMbMquDgdAM8I0TTxUO0o5ILF/gUyLT04R7QlOfktkdh6Qt0atTS\+xeKi1hirKRizpJ8jjnxGQIikPRToL2v3ZZZZZZ=='\}  # pragma: allowlist secret
action\_result\.data\.\*\.TableNames | string |  |  
action\_result\.data\.\*\.ResponseMetadata\.RequestId | string |  |   FE7CQFQDIO70P8CT6LHSH1J8NBVV4KQNSO5AEMVJF66Q9ASUAAJG 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.date | string |  |   Thu, 22 Sep 2022 10\:01\:09 GMT 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.server | string |  |   Server 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.connection | string |  |   keep\-alive 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.x\-amz\-crc32 | string |  |   2745614147 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-type | string |  |   application/x\-amz\-json\-1\.0 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-length | string |  |   2 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.x\-amzn\-requestid | string |  |   FE7CQFQDIO70P8CT6LHSH1J8NBVV4KQNSO5AEMVJF66Q9ASUAAJG 
action\_result\.data\.\*\.ResponseMetadata\.RetryAttempts | numeric |  |   0 
action\_result\.data\.\*\.ResponseMetadata\.HTTPStatusCode | numeric |  |   200 
action\_result\.message | string |  |   Updated item successfully 
action\_result\.summary | string |  |  
summary\.total\_objects | numeric |  |   1 
summary\.total\_objects\_successful | numeric |  |   1   

## action: 'get item'
Get an item from the table

Type: **investigate**  
Read only: **True**

We don't need to pass value in encoded format for the parameters\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**table\_name** |  required  | Name of table from which you want to fetch item | string |  `aws dynamodb table name` 
**partition\_key\_name** |  required  | Name of partition key | string |  `aws dynamodb partition key name` 
**sort\_key\_name** |  optional  | Name of sort key | string |  `aws dynamodb sort key name` 
**partition\_key\_value** |  required  | Partition key value | string | 
**sort\_key\_value** |  optional  | Sort key value | string | 
**partition\_key\_datatype** |  required  | Partition key datatype | string | 
**sort\_key\_datatype** |  optional  | Sort key datatype | string | 
**attributes\_to\_get** |  optional  | To fetch specific attributes from the item | string | 
**reserved\_keyword\_attributes** |  optional  | To fetch attributes from items whose names are same as reserved keywords | string | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action\_result\.status | string |  |   success  failed 
action\_result\.parameter\.table\_name | string |  `aws dynamodb table name`  |   test\_dev\_table 
action\_result\.parameter\.partition\_key\_name | string |  `aws dynamodb partition key name`  |   testing1 
action\_result\.parameter\.partition\_key\_value | string |  |   2 
action\_result\.parameter\.sort\_key\_name | string |  `aws dynamodb sort key name`  |  
action\_result\.parameter\.sort\_key\_value | string |  |  
action\_result\.parameter\.partition\_key\_datatype | string |  |   String 
action\_result\.parameter\.sort\_key\_datatype | string |  |  
action\_result\.parameter\.attributes\_to\_get | string |  |  
action\_result\.parameter\.reserved\_keyword\_attributes | string |  |  
action\_result\.parameter\.credentials | string |  `aws credentials`  |   \{'AccessKeyId'\: 'ASIASJL6ZZZZZ3M7QC2J', 'Expiration'\: '2021\-06\-07 22\:28\:04', 'SecretAccessKey'\: 'ZZZZZAmvLPictcVBPvjJx0d7MRezOuxiLCMZZZZZ', 'SessionToken'\: 'ZZZZZXIvYXdzEN///////////wEaDFRU0s4AVrw0k0oYICK4ATAzOqzAkg9bHY29lYmP59UvVOHjLufOy4s7SnAzOxGqGIXnukLis4TWNhrJl5R5nYyimrm6K/9d0Cw2SW9gO0ZRjEJHWJ\+yY5Qk2QpWctS2BGn4n\+G8cD6zEweCCMj\+ScI5p8n7YI4wOdvXvOsVMmjV6F09Ujqr1w\+NwoKXlglznXGs/7Q1kNZOMiioEhGUyoiHbQb37GCKslDK\+oqe0KNaUKQ96YCepaLgMbMquDgdAM8I0TTxUO0o5ILF/gUyLT04R7QlOfktkdh6Qt0atTS\+xeKi1hirKRizpJ8jjnxGQIikPRToL2v3ZZZZZZ=='\}  # pragma: allowlist secret
action\_result\.data\.\*\.TableNames | string |  |  
action\_result\.data\.\*\.Item | string |  |  
action\_result\.data\.\*\.ResponseMetadata\.RequestId | string |  |   EITIHSOAI9VTL2VPB08G059K63VV4KQNSO5AEMVJF66Q9ASUAAJG 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.date | string |  |   Thu, 22 Sep 2022 05\:59\:54 GMT 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.server | string |  |   Server 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.connection | string |  |   keep\-alive 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.x\-amz\-crc32 | string |  |   4263225874 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-type | string |  |   application/x\-amz\-json\-1\.0 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-length | string |  |   106 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.x\-amzn\-requestid | string |  |   EITIHSOAI9VTL2VPB08G059K63VV4KQNSO5AEMVJF66Q9ASUAAJG 
action\_result\.data\.\*\.ResponseMetadata\.RetryAttempts | numeric |  |   0 
action\_result\.data\.\*\.ResponseMetadata\.HTTPStatusCode | numeric |  |   200 
action\_result\.message | string |  |   Fetched Item Data Successfully 
action\_result\.summary | string |  |  
summary\.total\_objects | numeric |  |   1 
summary\.total\_objects\_successful | numeric |  |   1   

## action: 'query data'
Query data from database

Type: **investigate**  
Read only: **True**

<ul><li>Select Parameter<ul><li>The select parameter defines what attributes are supposed to fetched\. There are following options \:</li><ul><li><b>ALL\_ATTRIBUTES</b> \: Returns all of the item attributes from the specified table or index\. If you query a local secondary index, then for each matching item in the index, DynamoDB fetches the entire item from the parent table\. If the index is configured to project all item attributes, then all of the data can be obtained from the local secondary index, and no fetching is required\.</li><li><b>ALL\_PROJECTED\_ATTRIBUTES</b> \: Allowed only when querying an index\. Retrieves all attributes that have been projected into the index\. If the index is configured to project all attributes, this return value is equivalent to specifying ALL\_ATTRIBUTES</li><li><b>COUNT</b> \: Returns the number of matching items, rather than the matching items themselves</li><li><b>SPECIFIC\_ATTRIBUTES</b> \: Returns only the attributes listed in ProjectionExpression\. This return value is equivalent to specifying ProjectionExpression without specifying any value for Select</li></ul><li>If you use the <b>ProjectionExpression</b> parameter, then the value for Select can only be SPECIFIC\_ATTRIBUTES\. Any other value for Select will return an error\.</li></ul></li><li>Return Consumed Capacity Parameter<ul><li>Determines the level of detail about either provisioned or on\-demand throughput consumption that is returned in the response\. There are following options \:</li><ul><li>INDEXES \- The response includes the aggregate ConsumedCapacity for the operation, together withConsumedCapacity for each table and secondary index that was accessed\.</li><li>TOTAL \- The response includes only the aggregate ConsumedCapacity for the operation\.</li><li>NONE \- No ConsumedCapacity details are included in the response\.</li></ul></ul></li><li>KeyConditionExpression Parameter<ul><li></li></ul></li></ul>

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**table\_name** |  required  | Name of Table to perform query on | string |  `aws dynamodb table name` 
**index\_name** |  optional  | Name of index to be used for the query | string | 
**expression\_attribute\_names** |  optional  | Attribute names json | string | 
**expression\_attribute\_values** |  optional  | Attribute values json | string | 
**key\_condition\_expression** |  required  | Attribute values json | string | 
**filter\_expression** |  optional  | Expression to filter data from table\.A FilterExpression does not allow key attributes\. You cannot define a filter expression based on a partition key or a sort key\. | string | 
**projection\_expression** |  optional  | Defines the attributes to be included in the result\. If this expression is provided SELECT value is set to SPECIFIC\_ATTRIBUTES\. The attributes in the expression must be separated by commas\. | string | 
**select** |  optional  | Retrieve all item attributes, specific item attributes, the count of matching items, or in the case of an index, some or all of the attributes projected into the index\. | string | 
**return\_consumed\_capacity** |  optional  | Determines the level of detail about either provisioned or on\-demand throughput consumption that is returned in the response | string | 
**max\_items** |  optional  | Maximum number of items to process | numeric | 
**sort\_descending** |  optional  | By default, the sort order for query data is ascending\. To reverse the order, set the sort\_descending parameter to true\. | boolean | 
**consistent\_read** |  optional  | Determines the read consistency model\: If set to true, then the operation uses strongly consistent reads; otherwise, the operation uses eventually consistent reads | boolean | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action\_result\.status | string |  |   success  failed 
action\_result\.parameter\.table\_name | string |  `aws dynamodb table name`  |   test\_query 
action\_result\.parameter\.index\_name | string |  |  
action\_result\.parameter\.expression\_attribute\_names | string |  |   \{ "\#fn" \:  "firstname"\} 
action\_result\.parameter\.expression\_attribute\_values | string |  |   \{"\:fn" \: \{ "S" \: "testdata"\}\} 
action\_result\.parameter\.key\_condition\_expression | string |  |   \#fn  =  \:fn 
action\_result\.parameter\.filter\_expression | string |  |  
action\_result\.parameter\.projection\_expression | string |  |  
action\_result\.parameter\.select | string |  |   ALL\_ATTRIBUTES 
action\_result\.parameter\.consistent\_read | boolean |  |   False 
action\_result\.parameter\.sort\_descending | boolean |  |   False 
action\_result\.parameter\.return\_consumed\_capacity | string |  |  
action\_result\.parameter\.max\_items | numeric |  |   2 
action\_result\.parameter\.credentials | string |  `aws credentials`  |   \{'AccessKeyId'\: 'ASIASJL6ZZZZZ3M7QC2J', 'Expiration'\: '2021\-06\-07 22\:28\:04', 'SecretAccessKey'\: 'ZZZZZAmvLPictcVBPvjJx0d7MRezOuxiLCMZZZZZ', 'SessionToken'\: 'ZZZZZXIvYXdzEN///////////wEaDFRU0s4AVrw0k0oYICK4ATAzOqzAkg9bHY29lYmP59UvVOHjLufOy4s7SnAzOxGqGIXnukLis4TWNhrJl5R5nYyimrm6K/9d0Cw2SW9gO0ZRjEJHWJ\+yY5Qk2QpWctS2BGn4n\+G8cD6zEweCCMj\+ScI5p8n7YI4wOdvXvOsVMmjV6F09Ujqr1w\+NwoKXlglznXGs/7Q1kNZOMiioEhGUyoiHbQb37GCKslDK\+oqe0KNaUKQ96YCepaLgMbMquDgdAM8I0TTxUO0o5ILF/gUyLT04R7QlOfktkdh6Qt0atTS\+xeKi1hirKRizpJ8jjnxGQIikPRToL2v3ZZZZZZ=='\}  # pragma: allowlist secret
action\_result\.data\.\*\.TableNames | string |  |  
action\_result\.data\.\*\.QueryData | string |  |  
action\_result\.message | string |  |   Fetched data successfully 
action\_result\.summary | string |  |  
summary\.total\_objects | numeric |  |   1 
summary\.total\_objects\_successful | numeric |  |   1   

## action: 'test connectivity'
Validate the asset configuration for connectivity using the supplied configuration

Type: **test**  
Read only: **True**

#### Action Parameters
No parameters are required for this action

#### Action Output
No Output