import boto3
import json
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('UrlMappings')

def lambda_handler(event, context):
    try:
        short_id = None
        if event.get("pathParameters"):
            short_id = event["pathParameters"].get("shortId")

        if not short_id:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing shortId in request"})
            }

        response = table.get_item(Key={"shortId": short_id})
        item = response.get("Item")

        if not item:
            return {
                "statusCode": 404,
                "body": json.dumps({"error": "Short URL not found"})
            }

        return {
            "statusCode": 200,
            "body": json.dumps({
                "shortId": short_id,
                "longUrl": item["longUrl"],
                "clickCount": int(item["clickCount"]),   # force to int
                "createdAt": item.get("createdAt", "N/A")
            }, default=str)
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
