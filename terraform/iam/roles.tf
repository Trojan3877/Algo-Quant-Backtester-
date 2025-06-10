# terraform/iam/roles.tf

resource "aws_iam_role" "ci_cd_role" {
  name               = "${var.project_name}-ci-cd-role"
  assume_role_policy = data.aws_iam_policy_document.ci_cd_assume.json
  description        = "Role assumed by GitHub Actions for CI/CD deployments"
}

data "aws_iam_policy_document" "ci_cd_assume" {
  statement {
    effect = "Allow"
    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com", "ecs-tasks.amazonaws.com"]
    }
    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "eks_node_role" {
  name               = "${var.project_name}-eks-node-role"
  assume_role_policy = data.aws_iam_policy_document.eks_node_assume.json
  description        = "Role for EKS worker nodes"
}

data "aws_iam_policy_document" "eks_node_assume" {
  statement {
    effect = "Allow"
    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "mlflow_s3_role" {
  name               = "${var.project_name}-mlflow-s3-role"
  assume_role_policy = data.aws_iam_policy_document.mlflow_s3_assume.json
  description        = "Role for MLflow server to access S3 artifacts"
}

data "aws_iam_policy_document" "mlflow_s3_assume" {
  statement {
    effect = "Allow"
    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com", "ec2.amazonaws.com"]
    }
    actions = ["sts:AssumeRole"]
  }
}


mkdir -p terraform/iam
git add terraform/iam/roles.tf
git commit -m "Add IAM roles: CI/CD, EKS nodes, MLflow S3 access"
git push
