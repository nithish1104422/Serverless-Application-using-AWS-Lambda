import json
import boto3
from botocore.exceptions import ClientError

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ItemsTable')  # Replace with your DynamoDB table name

def lambda_handler(event, context):
    http_method = event['httpMethod']
    if http_method == 'GET':
        return get_items()
    elif http_method == 'POST':
        return add_item(event)
    elif http_method == 'DELETE':
        return delete_item(event)
    else:
        return {
            "statusCode": 405,
            "body": json.dumps({"error": "Method Not Allowed"})
        }

def get_items():
    try:
        response = table.scan()
        return {
            "statusCode": 200,
            "body": json.dumps(response['Items'])
        }
    except ClientError as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

def add_item(event):
    try:
        body = json.loads(event['body'])
        table.put_item(Item=body)
        return {
            "statusCode": 201,
            "body": json.dumps({"message": "Item added successfully"})
        }
    except ClientError as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

def delete_item(event):
    try:
        body = json.loads(event['body'])
        key = body.get('id')
        if not key:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing id in request"})
            }
        table.delete_item(Key={"id": key})
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Item deleted successfully"})
        }
    except ClientError as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
