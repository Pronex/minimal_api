# terraform main file

# configure azure provider
provider "azurerm" {
  features {}
}

# base resources
# main resource group
resource "azurerm_resource_group" "rg_main" {
  name     = var.tf_rg
  location = var.default_location
}
