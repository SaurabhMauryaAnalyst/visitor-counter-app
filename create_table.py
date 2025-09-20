# create_table.py
import boto3, os
from botocore.exceptions import ClientError

AWS_REGION = os.getenv("AWS_REGION","us-east-1")
DDB_ENDPOINT = os.getenv("DYNAMODB_ENDPOINT")  # optional

if DDB_ENDPOINT:
    client = boto3.client("dynamodb", region_name=AWS_REGION, endpoint_url=DDB_ENDPOINT)
else:
    client = boto3.client("dynamodb", region_name=AWS_REGION)

table_name = os.getenv("DDB_TABLE", "VisitorCount")

try:
    client.create_table(
        TableName=table_name,
        AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
        KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
        BillingMode="PAY_PER_REQUEST",
    )
    print(f"Creating table {table_name}...")
    waiter = client.get_waiter('table_exists')
    waiter.wait(TableName=table_name)
    print("Table ready.")
except ClientError as e:
    if e.response['Error']['Code'] == 'ResourceInUseException':
        print("Table already exists.")
    else:
        raise

# seed item (if not present)
try:
    client.put_item(
        TableName=table_name,
        Item={"id": {"S": "visitors"}, "visits": {"N": "0"}},
        ConditionExpression="attribute_not_exists(id)"
    )
    print("Seeded item.")
except ClientError as e:
    if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
        print("Seed item already exists.")
    else:
        raise
