import json
import boto3
import sys
import base64
sys.path.insert(1, '/opt')
import cv2
import time
timestr = time.strftime("%Y%m%d-%H%M%S")

def lambda_handler(event, context):
    fragments = []
    print(event)
    for record in event['Records']:
       #Kinesis data is base64 encoded so decode here
       payload=base64.b64decode(record["kinesis"]["data"])
       payload=json.loads(payload)
       print('Record -->', record)
       if len(payload['FaceSearchResponse']) > 0:
        fragments.append(payload["InputInformation"]["KinesisVideo"]["FragmentNumber"])
       print('Decoded payload: ' + str(payload))
    if len(fragments) == 0:
        return {
            'statusCode': 200,
            'body': json.dumps('No deteted faces!')
        }
    kvs_client = boto3.client('kinesisvideo')
    kvs_data_pt = kvs_client.get_data_endpoint(
        StreamARN='arn:aws:kinesisvideo:us-east-1:382782476131:stream/demo-stream/1573802511682', # kinesis stream arn
        APIName='GET_MEDIA'
    )
    print('fragments', fragments)

    end_pt = kvs_data_pt['DataEndpoint']
    kvs_video_client = boto3.client('kinesis-video-media', endpoint_url=end_pt, region_name='us-east-1') # provide your region
    kvs_stream = kvs_video_client.get_media(
        StreamARN='arn:aws:kinesisvideo:us-east-1:382782476131:stream/demo-stream/1573802511682', # kinesis stream arn
        StartSelector={'AfterFragmentNumber': fragments[0], 'StartSelectorType': 'FRAGMENT_NUMBER'} # to keep getting latest available chunk on the stream
    )

    with open('/tmp/stream.mkv', 'wb') as f:
        streamBody = kvs_stream['Payload'].read(1024*2048) # reads min(16MB of payload, payload size) - can tweak this
        print('GOT STREAM')
        f.write(streamBody)
        print('WROTE STREAM')
        # use openCV to get a frame

        s3_client = boto3.client('s3')
        s3_client.upload_file(
                '/tmp/stream.mkv',
                'list-of-faces',
                'video-1.mkv'
            )
        print("Uploaded video")

        cap = cv2.VideoCapture('/tmp/stream.mkv')

        # use some logic to ensure the frame being read has the person, something like bounding box or median'th frame of the video etc
        ret, frame = cap.read()
        if frame is not None:
            #cv2.imwrite('/tmp/frame.jpg', frame)
            s3_client = boto3.client('s3')
            img_name = 'frame-' + timestr + '.jpg'
            s3_client.upload_file(
                '/tmp/frame.jpg',
                'list-of-faces',
                img_name
            )
            print('Image uploaded')
        cap.release()
