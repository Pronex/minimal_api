# configure azure provider
provider "azurerm" {
  features {}
}

# Define Terraform backend using a blob storage container on Microsoft Azure for storing the Terraform state
terraform {
  backend "azurerm" {
    resource_group_name  = "rg-tfstate"
    storage_account_name = "tfstorraw"
    container_name       = "tfstate"
    key                  = "api.tfstate"
  }
}

# data sources
data "azurerm_container_registry" "acr-minimal-api" {
  name                = var.acr-minimal-api
  resource_group_name = var.rg-acr
}
