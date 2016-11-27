
import boto3
import json
from watson_developer_cloud import AlchemyLanguageV1

session = boto3.Session(
    aws_access_key_id='AKIAJ5IZKUVUKBGNQC5Q',
    aws_secret_access_key='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'
)
alchemy_language = AlchemyLanguageV1(api_key='c9dae3d9a28f23161fa9f8fbc0e0d08c4f6d1fb0')
sns = boto3.resource('sns', 'us-east-1')
sqs = boto3.resource('sqs', 'us-east-1')
queue = sqs.get_queue_by_name(QueueName='Tweet')
topic = sns.Topic('Tweet')
#print(queue.url)
#print(queue.attributes.get('DelaySeconds'))

queue.send_message(MessageBody='text23', MessageAttributes={
    'Lon': {
        'StringValue': 'longtitude23',
        'DataType': 'String'
    }
})

#print alchemy_language.sentiment(text='text')["docSentiment"]["type"]
