# terraform/variables.tf

variable "aws_region" {
  description = "The AWS region to deploy resources in"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Name of the project, used for naming resources"
  type        = string
  default     = "algoquant-backtester"
}

variable "owner" {
  description = "Owner or maintainer of the infrastructure"
  type        = string
  default     = "Corey Leath"
}

variable "vpc_id" {
  description = "The VPC ID where EKS and other resources will be deployed"
  type        = string
}

variable "subnet_ids" {
  description = "A list of subnet IDs for the EKS worker nodes"
  type        = list(string)
}

# Random ID provider for unique naming
terraform {
  required_providers {
    random = {
      source  = "hashicorp/random"
      version = "~> 3.0"
    }
  }
}

git add terraform/variables.tf
git commit -m "Add Terraform variables.tf"
git push
