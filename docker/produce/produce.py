import json
import tweepy
import boto3
import time
import os

# Set up Twitter API credentials using environment variables
consumer_key = os.environ['CONSUMER_KEY']
consumer_secret = os.environ['CONSUMER_SECRET']
access_token = os.environ['ACCESS_TOKEN']
access_token_secret = os.environ['ACCESS_TOKEN_SECRET']

# Authenticate with the Twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Initialize the Kinesis client and set the stream name
kinesis_client = boto3.client('kinesis', region_name='us-east-2')
kinesis_stream_name = 'kinesis_twitter_stream'

# Initialize the tweet counter
tweet_count = 0

# Search for recent tweets containing the keyword 'devops'
tweets = api.search(q='devops', lang='en', count=10)

# Check if there are any tweets
if not tweets:
    print('No tweets found.')

# Send each tweet to the Kinesis stream
for tweet in tweets:
    try:
        # Create a record for the Kinesis stream
        kinesis_record = {
            'Data': json.dumps(tweet._json),
            'PartitionKey': tweet.id_str
        }
        # Put the record into the Kinesis stream
        response = kinesis_client.put_record(StreamName=kinesis_stream_name, Data=json.dumps(kinesis_record),
                                             PartitionKey='partitionkey')
        # Print the record being sent to Kinesis
        print(f"Sending record to Kinesis: {json.dumps(kinesis_record)}")
        # Increment tweet counter
        tweet_count += 1
    except Exception as e:
        print(f"Failed to send tweet with id {tweet.id_str} to Kinesis. Error: {e}")

# Print the total number of tweets processed
print(f"{tweet_count} tweets processed.")

# Sleep for 30 seconds
time.sleep(30)
