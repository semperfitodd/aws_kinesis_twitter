#!/bin/bash

AWS_REGION=us-east-2
STREAM_NAME=kinesis_twitter_stream
TABLE_NAME=kinesis_twitter_table
TEST_DATA=test

echo " "
echo " "
echo " *************************************************"
echo " Putting record \"$TEST_DATA\" in"
echo " $STREAM_NAME in AWS REGION $AWS_REGION"
echo " *************************************************"
echo " "


SHARD_ID=$(aws --region $AWS_REGION \
kinesis put-record \
--stream-name $STREAM_NAME \
--partition-key 123 \
--data $TEST_DATA \
--query 'ShardId' \
--output text)

SHARD_ITERATOR=$(aws --region $AWS_REGION \
kinesis get-shard-iterator \
--shard-id $SHARD_ID \
--shard-iterator-type TRIM_HORIZON \
--stream-name $STREAM_NAME \
--query 'ShardIterator' \
--output text)

echo " "
echo " "
echo " *************************************************"
echo " Consuming record"
echo " *************************************************"
echo " "

SHARD_RECORD=$(aws --region $AWS_REGION \
kinesis get-records \
--shard-iterator $SHARD_ITERATOR \
--query 'Records[*].Data' \
--output text \
| awk '{print $1;}')

echo " "
echo " "
echo " *************************************************"
echo " Storing record in DynamoDB"
echo " *************************************************"
echo " "

aws --region $AWS_REGION \
dynamodb put-item \
--table-name $TABLE_NAME  \
--item \
'{"from_kinesis": {"S": "'${SHARD_RECORD}'"}}'

echo " "
echo " "
echo " *************************************************"
echo " SUCCESS!!!"
echo " *************************************************"
echo " "