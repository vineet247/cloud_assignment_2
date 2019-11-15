import json



def lambda_handler(event, context):

    lastUserMessage = event['message'];
    name=lastUserMessage['name']
    phone=lastUserMessage['phone']
    botMessage = "There is something wrong, Please start process once again.";

    if lastUserMessage is None or len(lastUserMessage) < 1:
        return {
            'statusCode': 200,
            'body': json.dumps(botMessage)
        }


    print(name)
    print(phone)


    return {
        'statusCode': 200,
        'body': json.dumps('We are adding this visitor')
    }
