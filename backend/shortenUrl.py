import json
import boto3
import string
import random
import time

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('UrlMappings')

def generate_short_id(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def lambda_handler(event, context):
    body = json.loads(event["body"])
    long_url = body.get("longUrl")

    if not long_url:
        return {"statusCode": 400, "body": json.dumps({"error": "Missing longUrl"})}

    short_id = generate_short_id()

    table.put_item(Item={
        "shortId": short_id,
        "longUrl": long_url,
        "clickCount": 0,
        "createdAt": str(int(time.time()))
    })

    return {
        "statusCode": 200,
        "body": json.dumps({"shortId": short_id, "longUrl": long_url})
    }
