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

def lambda_handler(event, context):
    otp = int(event['message'])
    #otp = 9460
    flagFound = False

    #resp = table.query(KeyConditionExpression=Key('faceId'))
    #resp = table.get_item(Key={'otp': otp})
    #filtering_exp = Key('otp').eq(otp)
    #resp = table.query(KeyConditionExpression=filtering_exp)

    filtering_exp = Key('otp').eq(otp)
    resp = table.scan(FilterExpression=filtering_exp)

    if(resp["Count"]!=0):
        print("The query returned the following items:")
        for item in resp['Items']:
            if item["otp"] == otp:
                visitorFaceId = item["faceId"]
                flagFound = True
    else:
        print("Not Found!")
    if(flagFound):
        resp1 = table1.query(KeyConditionExpression=Key('faceId').eq(visitorFaceId))
        if(resp1["Count"]!=0):
            for item1 in resp1['Items']:
                print("Welcome! "+item1["name"]+", You may enter the door!")
                return {
                            'statusCode': 200,
                            'body': json.dumps('Welcome '+item1["name"]+'! You may enter the door!')
                        }
    else:
        print("Sorry, your record is not present in the Visitors table!")
        return {
                        'statusCode': 200,
                        'body': json.dumps('Your OTP is wrong!')
                    }
