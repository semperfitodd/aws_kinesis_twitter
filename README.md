# AWS Kinesis Twitter stream

### Set up a Twitter developer account and create an app to obtain the necessary credentials (consumer key, consumer secret, access token, access token secret).
* Go to the Twitter Developer website: https://developer.twitter.com/
* Click on "Apply" in the top right corner.
* If you are not already logged in, you will be prompted to log in with your Twitter account. If you don't have a Twitter account, you will need to create one first.
* Once logged in, click on "Apply for a Developer Account."
* Choose the appropriate developer account type: "Hobbyist" or "Business." For most personal projects, the "Hobbyist" option is suitable. Click "Next."
* Fill out the required information about yourself, such as your name, country, and description. Click "Next."
* On the next page, you will be asked to provide details about your intended use of the Twitter API. Answer the questions about how you plan to use the API, including the purpose, features you plan to implement, and how you will analyze the data. Be as descriptive as possible, as Twitter will review your application based on your answers.
* Review the Developer Agreement and accept the terms by checking the box. Click "Submit Application" to submit your application for review.
* Once your application is submitted, you will receive an email from Twitter. Your application will be reviewed, and you should receive a response within a few days. If your application is approved, you will be granted access to the Twitter Developer Dashboard, where you can manage your apps and API keys.
### Create AWS services (DynamoDB and Kinesis)
```
cd terraform
terraform init
terraform plan -out=plan.out
terraform apply
```
### Build docker images from producer and consumer
```
cd docker
docker build -t twitter_produce -f Dockerfile_produce .
docker build -t twitter_consume -f Dockerfile_consume .
```
### Run docker containers for producer and consumer
* Create keys in the twitter developer console
* Mounting the credentials into the docker image will allow the docker image to have the appropriate permissions
* Producer will look for 10 most recent tweets with "devops" in the tweet
* Producer repeats every 30 seconds
* Consumer reads stream every 15 seconds
```
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
### Check records in Kinesis streams
![kinesis_records.png](images%2Fkinesis_records.png)
### Confirm records are consumed into DynamoDB
![dynamodb_records.png](images%2Fdynamodb_records.png)
### Clean up
```
docker stop twitter_produce
docker stop twitter_consume
docker system prune --force

terraform destroy
```