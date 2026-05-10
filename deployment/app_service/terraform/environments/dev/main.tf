module "rg" {
  source      = "git::https://github.com/ASHISH-ARORA-24/wings.git//deployment/app_service/terraform/modules/resource_group?ref=tf/v1.0.0"
  environment = "dev"
  location    = var.location
  project     = var.project
}
