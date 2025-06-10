terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# S3 bucket for DVC remote storage
resource "aws_s3_bucket" "dvc_bucket" {
  bucket = "${var.project_name}-dvc-${random_id.bucket_id.hex}"
  acl    = "private"
}

resource "random_id" "bucket_id" {
  byte_length = 4
}

# EKS Cluster
module "eks" {
  source          = "terraform-aws-modules/eks/aws"
  cluster_name    = var.project_name
  cluster_version = "1.24"
  subnets         = var.subnet_ids
  vpc_id          = var.vpc_id

  node_groups = {
    default = {
      desired_capacity = 2
      max_capacity     = 4
      min_capacity     = 1
      instance_types   = ["t3.medium"]
    }
  }

  tags = {
    Project = var.project_name
    Owner   = var.owner
  }
}


git add terraform/main.tf
git commit -m "Add Terraform main.tf for S3 bucket and EKS cluster"
git push
