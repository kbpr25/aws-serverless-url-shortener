import boto3
import json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('UrlMappings')

def lambda_handler(event, context):
    short_id = event["pathParameters"]["shortId"]


    response = table.get_item(Key={"shortId": short_id})
    item = response.get("Item")

    if not item:
        return {
            "statusCode": 404,
            "body": json.dumps({"error": "Short URL not found"})
        }

    # Increment click count
    table.update_item(
        Key={"shortId": short_id},
        UpdateExpression="SET clickCount = clickCount + :val",
        ExpressionAttributeValues={":val": 1}
    )

    return {
        "statusCode": 302,
        "headers": {"Location": item["longUrl"]},
        "body": ""
    }
