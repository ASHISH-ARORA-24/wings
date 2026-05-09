module "rg" {
  source      = "../../modules/resource_group"
  environment = "sandbox"
  location    = var.location
  project     = var.project
}
