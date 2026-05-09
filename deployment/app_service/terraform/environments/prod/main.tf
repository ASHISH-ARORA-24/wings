# Module source will be updated to GitHub URL after tagging:
# source = "git::https://github.com/AshishArora24/wings.git//deployment/app_service/terraform/modules/resource_group?ref=v0.1.0"

module "rg" {
  source      = "../../modules/resource_group"
  environment = "prod"
  location    = var.location
  project     = var.project
}
