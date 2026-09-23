terraform {
  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.35"
    }
  }
}

provider "kubernetes" {
  config_path = "~/.kube/config"
}
resource "kubernetes_namespace" "gitops" {
  metadata {
    name = var.namespace_name
  }
}
resource "kubernetes_config_map" "platform_config" {
  metadata {
    name      = "platform-config"
    namespace = kubernetes_namespace.gitops.metadata[0].name
  }

  data = {
    APP_NAME = "GitOps Platform"
    ENV      = "development"
  }
}
resource "kubernetes_service_account" "gitops" {
  metadata {
    name      = "gitops-platform"
    namespace = kubernetes_namespace.gitops.metadata[0].name
  }
}