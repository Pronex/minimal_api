# Define Terraform backend using a blob storage container on Microsoft Azure for storing the Terraform state
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.50"
    }
  }

  backend "azurerm" {
    resource_group_name  = "rg-tfstate"
    storage_account_name = "tfstorraw"
    container_name       = "tfstate"
    key                  = "api.tfstate"
  }
}
