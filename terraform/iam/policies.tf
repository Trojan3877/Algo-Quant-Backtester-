# terraform/iam/policies.tf

# CI/CD Role Policy: allow EKS, ECR, S3, Terraform operations
resource "aws_iam_policy" "ci_cd_policy" {
  name        = "${var.project_name}-ci-cd-policy"
  description = "Policy for GitHub Actions CI/CD"
  policy      = data.aws_iam_policy_document.ci_cd_policy.json
}

data "aws_iam_policy_document" "ci_cd_policy" {
  statement {
    actions = [
      "ecr:GetAuthorizationToken",
      "ecr:BatchCheckLayerAvailability",
      "ecr:GetDownloadUrlForLayer",
      "ecr:BatchGetImage",
      "ecr:PutImage",
      "ecr:InitiateLayerUpload",
      "ecr:UploadLayerPart",
      "ecr:CompleteLayerUpload",
      "eks:DescribeCluster",
      "eks:ListClusters",
      "eks:DescribeNodegroup",
      "eks:ListNodegroups",
      "s3:ListBucket",
      "s3:GetObject",
      "s3:PutObject"
    ]
    resources = ["*"]
  }
}

resource "aws_iam_role_policy_attachment" "ci_cd_attach" {
  role       = aws_iam_role.ci_cd_role.name
  policy_arn = aws_iam_policy.ci_cd_policy.arn
}

# EKS Node Role Policy: managed AWS policy
resource "aws_iam_role_policy_attachment" "eks_node_attach" {
  role       = aws_iam_role.eks_node_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy"
}

resource "aws_iam_role_policy_attachment" "eks_cni_attach" {
  role       = aws_iam_role.eks_node_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy"
}

resource "aws_iam_role_policy_attachment" "ec2_attach" {
  role       = aws_iam_role.eks_node_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
}

# MLflow S3 Role Policy: allow S3 bucket access
resource "aws_iam_policy" "mlflow_s3_policy" {
  name        = "${var.project_name}-mlflow-s3-policy"
  description = "Policy for MLflow server to access DVC S3 bucket"
  policy      = data.aws_iam_policy_document.mlflow_s3_policy.json
}

data "aws_iam_policy_document" "mlflow_s3_policy" {
  statement {
    actions = [
      "s3:ListBucket",
      "s3:GetObject",
      "s3:PutObject"
    ]
    resources = [
      aws_s3_bucket.dvc_bucket.arn,
      "${aws_s3_bucket.dvc_bucket.arn}/*"
    ]
  }
}

resource "aws_iam_role_policy_attachment" "mlflow_s3_attach" {
  role       = aws_iam_role.mlflow_s3_role.name
  policy_arn = aws_iam_policy.mlflow_s3_policy.arn
}


git add terraform/iam/policies.tf
git commit -m "Add IAM policies and attachments for CI/CD, EKS nodes, MLflow"
git push
