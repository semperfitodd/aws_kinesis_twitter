import boto3
import json
import time
from datetime import datetime

dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
table_name = 'kinesis_twitter_table'
stream_name = 'kinesis_twitter_stream'


def process_record(record, kinesis):
    try:
        kinesis_data = json.loads(record['Data'])
        tweet_data = json.loads(kinesis_data['Data'])

        # Check if the tweet has an 'id_str' field
        if 'id_str' not in tweet_data:
            print('Skipping record - no id_str field')
            return

        # Extract relevant fields from tweet
        tweet_id = tweet_data['id_str']
        timestamp = datetime.strptime(tweet_data['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
        text = tweet_data['text']
        user = tweet_data['user']

        # Put data into DynamoDB
        table = dynamodb.Table(table_name)
        item = {
            'id': tweet_id,
            'timestamp': timestamp.isoformat(),
            'text': text,
            'user': {
                'id': user['id_str'],
                'screen_name': user['screen_name'],
                'name': user['name']
            }
        }
        table.put_item(Item=item)

    except Exception as e:
        print(f'Error processing record: {e}')


def process_shard(shard_id):
    kinesis = boto3.client('kinesis', region_name='us-east-2')
    shard_iterator = kinesis.get_shard_iterator(
        StreamName=stream_name,
        ShardId=shard_id,
        ShardIteratorType='TRIM_HORIZON'
    )['ShardIterator']

    while True:
        response = kinesis.get_records(ShardIterator=shard_iterator, Limit=25)

        if not response['Records']:
            break

        for record in response['Records']:
            process_record(record, kinesis)

        shard_iterator = response['NextShardIterator']
        time.sleep(1)


def main():
    kinesis = boto3.client('kinesis', region_name='us-east-2')
    response = kinesis.list_shards(StreamName=stream_name)
    shards = response['Shards']

    while True:
        if not shards:
            response = kinesis.list_shards(StreamName=stream_name)
            shards = response['Shards']

        for shard in shards:
            print(f'Processing shard: {shard["ShardId"]}')
            process_shard(shard['ShardId'])

        shards = None
        time.sleep(15)


if __name__ == '__main__':
    main()
