locals {
  environment = replace(var.environment, "_", "-")
}

variable "aws_region" {
  description = "AWS Region to deploy resources"
  default     = "us-east-2"
}

variable "environment" {
  description = "Environment name we are building"
  default     = "kinesis_twitter"
}

variable "my_name" {
  description = "My name"
  default     = "Todd Bernson"
}

variable "tags" {
  description = "Default tags for this environment"
  default     = {}
}