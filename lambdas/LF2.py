import json
import boto3
import time
from boto3.dynamodb.conditions import Key
import random


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('passcodes')
table1 = dynamodb.Table('visitors')

def lambda_handler(event, context):
    value1 = random.randint(0, 9)
    value2 = random.randint(0, 9)
    value3 = random.randint(0, 9)
    value4 = random.randint(0, 9)
    otp = int(str(value1)+str(value2)+str(value3)+str(value4))
    #print("The OTP generated is : " + otp)
    faceId = "877"
    creationTime = int(time.time())
    expirationTime = int(time.time()) + 500000
    name = "KT"
    phoneNumber = "2015151935"

    response = table.put_item(
        Item={
                'faceId': faceId,
                'otp': otp,
                'creationTime': creationTime,
                'expirationTime': expirationTime
            }
        )
    response1 = table1.put_item(
        Item={
                'faceId': faceId,
                'name': name,
                'phoneNumber': phoneNumber,
                #'photos': photos
            }
        )
    phoneService(otp)
    return {
        'statusCode': 200,
        'body': json.dumps('Added and Tested Succesfully new one!')
    }


def phoneService(otp):
    #print(requestData['Phone']['StringValue'])
    sns = boto3.client('sns')
    topic_name = 'OtpSMS'
    # topic = sns.create_topic(Name = topic_name)
    #msg = textString
    msg = "Hello Teja! Here's your OTP for the door access : " + str(otp)
    #tpcArn = 'arn:aws:sns:us-east-1:962205162141:'+topic_name
    tpcArn = 'arn:aws:sns:us-east-1:382782476131:OtpSMS'
    #contact = '+19736418745'
    subs = sns.subscribe(
        TopicArn=tpcArn,
        Protocol='sms',
        Endpoint = '+12015151771'
        #Endpoint= '+1'+requestData['Phone']['StringValue']  # <-- number who'll receive an SMS message.
    )
    response = sns.publish(
    TopicArn = 'arn:aws:sns:us-east-1:382782476131:OtpSMS',
    Message=msg)
    # Print out the response
    return
   
