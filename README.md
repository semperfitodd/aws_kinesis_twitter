# AWS Kinesis Twitter Stream

This project demonstrates how to create a real-time data processing pipeline using AWS Kinesis, Twitter API, and DynamoDB. The pipeline fetches tweets based on a specific keyword (e.g., "devops") and streams the data into AWS Kinesis. The Kinesis stream is then consumed by a separate process, which stores the tweets in a DynamoDB table. The producer and consumer processes are containerized using Docker for easy deployment and management.

Follow the steps below to set up the project and get it running.

## Set up a Twitter Developer Account and Create an App

1. Visit the Twitter Developer website: https://developer.twitter.com/
2. Click on "Apply" in the top right corner.
3. Log in with your Twitter account or create one if you don't have one.
4. Click on "Apply for a Developer Account."
5. Choose the "Hobbyist" or "Business" developer account type and click "Next."
6. Fill out the required information about yourself and click "Next."
7. Provide details about your intended use of the Twitter API and click "Next."
8. Review the Developer Agreement, accept the terms, and click "Submit Application."
9. Wait for a response from Twitter on your application approval.

## Create AWS Services (DynamoDB and Kinesis)

Navigate to the `terraform` directory and execute the following commands:

```bash
cd terraform
terraform init
terraform plan -out=plan.out
terraform apply
```

## Build docker images from producer and consumer

Navigate to the docker directory and build the Docker images:

```bash
cd docker
docker build -t twitter_produce -f Dockerfile_produce .
docker build -t twitter_consume -f Dockerfile_consume .
```

Obtain your Twitter API keys from the Twitter Developer Console.
Mount the AWS credentials into the Docker container.
The producer searches for the 10 most recent tweets with "devops" and repeats every 30 seconds.
The consumer reads the Kinesis stream every 15 seconds.

```bash
docker run -d --name twitter_produce \
  -e CONSUMER_KEY='<consumer_key_from_twitter>' \
  -e CONSUMER_SECRET='<consumer_secret_from_twitter>' \
  -e ACCESS_TOKEN='<access_token_from_twitter>' \
  -e ACCESS_TOKEN_SECRET='<access_token_secret_from_twitter>' \
  twitter_produce
  
docker run -d --name twitter_consume \
  -v ~/.aws/credentials:/root/.aws/credentials:ro \
  -e AWS_PROFILE=<profile_name> \
  twitter_consume
```

## Verify Kinesis and DynamoDB Records

1. Check the records in the Kinesis stream.
![kinesis_records.png](images%2Fkinesis_records.png)
2. Confirm the records are consumed into DynamoDB.
![dynamodb_records.png](images%2Fdynamodb_records.png)

## Clean up

Stop the Docker containers, remove unused resources, and destroy the infrastructure:

```bash
docker stop twitter_produce
docker stop twitter_consume
docker system prune --force

terraform destroy
```

This documentation provides a step-by-step guide to setting up a Twitter Developer account, creating AWS services, building Docker images for producer and consumer, running the Docker containers, verifying Kinesis and DynamoDB records, and cleaning up the resources.