output "namespace_name" {
  description = "The Kubernetes namespace managed by Terraform"
  value       = kubernetes_namespace.gitops.metadata[0].name
}