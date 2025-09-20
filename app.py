# app.py
from flask import Flask
import boto3
import os
from decimal import Decimal

app = Flask(__name__)

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
DDB_TABLE = os.getenv("DDB_TABLE", "VisitorCount")
DDB_ENDPOINT = os.getenv("DYNAMODB_ENDPOINT")  # e.g., http://localhost:8000 for local dev

if DDB_ENDPOINT:
    dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION, endpoint_url=DDB_ENDPOINT)
else:
    dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)

table = dynamodb.Table(DDB_TABLE)

@app.route("/")
def home():
    try:
        # increments 'visits' by 1 atomically
        resp = table.update_item(
            Key={"id": "visitors"},
            UpdateExpression="ADD visits :inc",
            ExpressionAttributeValues={":inc": 1},
            ReturnValues="UPDATED_NEW",
        )
        visits = int(resp["Attributes"]["visits"])
        error = None
    except Exception as e:
        visits = "N/A"
        error = str(e)

    return f"""
    <html>
      <head><title>Visitor Counter</title></head>
      <body style="font-family:Arial; text-align:center; margin-top:50px;">
        <h1>🚀 Visitor Counter</h1>
        <h2>You are visitor #{visits}</h2>
        {f"<p style='color:red'>Error: {error}</p>" if error else ""}
      </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
