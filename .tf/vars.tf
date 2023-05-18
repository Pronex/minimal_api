# Type: Terraform Variables

# base variables
variable "app_name" {
  type        = string
  description = "Name of the app (used for naming resources)"
  default     = "minimal-api"
}

variable "default_location" {
  type        = string
  default     = "Westeurope"
  description = "Azure Region"
}

variable "rg-app" {
  type        = string
  description = "Resource Group name for resources to be created"
}

variable "rg-acr" {
  type        = string
  description = "Resource Group name for Azure Container Registry"
}

variable "acr-minimal-api" {
  type        = string
  description = "Azure Container Registry name"
}

# secrets
variable "uname" {
  type        = string
  description = "App environment: UNAME"
}

variable "pword" {
  type        = string
  description = "App environment: PWORD"
}

# tags
variable "prd_tags" {
  type = map(string)
  default = {
    "env"         = "prod"
    "application" = "minimal_api"
  }
}
