from __future__ import print_function
from PIL import Image
import requests
from io import BytesIO
import base64
import json
import boto3
import random
import time
from boto3.dynamodb.conditions import Key

print('Loading function')

# KT'S PART ----------------- SCROLL DOWN FOR YOUR PART
def phoneServiceKnown(otp,phoneNumber):
    #print(requestData['Phone']['StringValue'])
    sns = boto3.client('sns')
    topic_name = 'knownOtpSMS'
    # topic = sns.create_topic(Name = topic_name)
    #msg = textString
    msg = "Hello! Here's your OTP for the door access : " + str(otp)
    #tpcArn = 'arn:aws:sns:us-east-1:962205162141:'+topic_name
    tpcArn = 'arn:aws:sns:us-east-1:382782476131:knownOtpSMS'
    #contact = '+19736418745'
    subs = sns.subscribe(
        TopicArn=tpcArn,
        Protocol='sms',
        Endpoint = phoneNumber
        #Endpoint= '+1'+requestData['Phone']['StringValue']  # <-- number who'll receive an SMS message.
    )
    response = sns.publish(
    TopicArn = 'arn:aws:sns:us-east-1:382782476131:knownOtpSMS',
    Message=msg)
    # Print out the response
    return

def phoneServiceUnknown(msg):
    #print(requestData['Phone']['StringValue'])
    sns = boto3.client('sns')
    topic_name = 'unknownOtpSMS'
    # topic = sns.create_topic(Name = topic_name)
    #msg = textString
    #tpcArn = 'arn:aws:sns:us-east-1:962205162141:'+topic_name
    tpcArn = 'arn:aws:sns:us-east-1:382782476131:unknownOtpSMS'
    #contact = '+19736418745'
    subs = sns.subscribe(
        TopicArn=tpcArn,
        Protocol='sms',
        Endpoint = '+16468948286'
        #Endpoint= '+1'+requestData['Phone']['StringValue']  # <-- number who'll receive an SMS message.
    )
    response = sns.publish(
    TopicArn = 'arn:aws:sns:us-east-1:382782476131:unknownOtpSMS',
    Message=msg)
    # Print out the response
    return

# VINEET'S PART BELOW ------------ DO NOT TOUCH CODE ABOVE THAT IS KT'S

def lambda_handler(event, context):

    knownVisitor = True
    if(knownVisitor):

        #client = boto3.client('s3')
        #response = client.put_object(ACL='public-read', Bucket='list-of-faces', Body='https://shreekrishnatejagaraga.s3.amazonaws.com/rfAtDoor.jpg', Key='visitorFace.jpg',ContentType='image/jpeg')


        responses = requests.get('https://shreekrishnatejagaraga.s3.amazonaws.com/rfAtDoor.jpg')
        img = Image.open(BytesIO(responses.content))










        value1 = random.randint(0, 9)
        value2 = random.randint(0, 9)
        value3 = random.randint(0, 9)
        value4 = random.randint(0, 9)
        otp = int(str(value1)+str(value2)+str(value3)+str(value4))
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('passcodes')
        phoneNumber = '+12015151771'
        ts = int(time.time())
        ets = ts + 30000
        #testUserFaceId = "675"
        response = table.put_item(
        Item={
                'faceId': "877",
                'otp': otp,
                'creationTime': ts,
                'expirationTime': ets
            }
        )
        #phoneServiceKnown(otp,phoneNumber)
    else:
        msg = "Hello Owner! Looks like you've got a new visitor at the door. Please use link to authorise : " + "https://addvisitorwebpage.s3.amazonaws.com/index.html"
        #phoneServiceUnknown(msg)

    return
