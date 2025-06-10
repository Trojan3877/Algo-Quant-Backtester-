# terraform/outputs.tf

output "dvc_s3_bucket_name" {
  description = "Name of the S3 bucket used for DVC remote storage"
  value       = aws_s3_bucket.dvc_bucket.bucket
}

output "eks_cluster_name" {
  description = "Name of the EKS cluster"
  value       = module.eks.cluster_id
}

output "eks_cluster_endpoint" {
  description = "Endpoint of the EKS cluster"
  value       = module.eks.cluster_endpoint
}

output "eks_cluster_auth" {
  description = "Authentication configuration for the EKS cluster"
  value       = module.eks.cluster_authenticator
}

output "kubeconfig" {
  description = "Generated kubeconfig to access the EKS cluster"
  value       = module.eks.kubeconfig
  sensitive   = true
}


git add terraform/outputs.tf
git commit -m "Add Terraform outputs.tf"
git push
