terraform {
  backend "azurerm" {
    resource_group_name  = "rg-wings-tfstate"
    storage_account_name = "stwingstfstate"
    container_name       = "tfstate"
    key                  = "wings-dev.tfstate"
  }
}
