terraform {
  backend "s3" {
    bucket = "bsc.sandbox.terraform.state"
    key    = "kinesis_twitter"
    region = "us-east-2"
  }
}