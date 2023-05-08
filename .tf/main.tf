# terraform main file

# configure azure provider
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.11"
    }
  }

  backend "azurerm" {
    resource_group_name  = "rg-raw-terraform_state"
    storage_account_name = "stacctfstate"
    container_name       = "tfstate"
    key                  = "api.tfstate"
  }

}

provider "azurerm" {
  features {}
}