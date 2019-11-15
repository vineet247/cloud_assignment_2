import json
import boto3
import time
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('passcodes')
table1 = dynamodb.Table('visitors')
ts = int(time.time())
ets = ts + 30000
#testUserFaceId = "675"
flagFound = False
def lambda_handler(event, context):
    otp = event['message'];
    response = table.put_item(
        Item={
                'faceId': "700",
                'otp': 6810,
                'creationTime': ts,
                'expirationTime': ets

        }
    )
    video_id = 25
    resp = table.query(
                        IndexName='faceId',
                        KeyConditionExpression=Key('otp').eq(otp)
                    )

    if(resp["Count"]!=0):
        print("The query returned the following items:")
        for item in resp['Items']:
            visitorFaceId = item["faceId"]
            flagFound = True
    else:
        print("Not Found!")
    if(flagFound):
        resp1 = table1.query(KeyConditionExpression=Key('faceId').eq(visitorFaceId))
    if(resp1["Count"]!=0):
        for item1 in resp1['Items']:
            print("Welcome! "+item1["name"]+", You may enter the door!")
    else:
        print("Sorry, your record is not present in the Visitors table!")


    return {
        'statusCode': 200,
        'body': json.dumps('Added and Tested Succesfully new one!')
    }
