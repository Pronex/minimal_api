# Type: Terraform Variables

# base variables
variable "default_location" {
  type        = string
  default     = "Westeurope"
  description = "Azure Region"
}

variable "tf_rg" {
  type        = string
  default     = "rg-tfstate"
  description = "Resource Group name for the terraform state"
}

variable "main_rg" {
  type        = string
  default     = "rg-mini-api"
  description = "Resource Group name for resources"
}

# secrets
# variable "some_secret" {
#   type = string
#   description = "Some secret value"
# }

# tags
variable "prd_tags" {
  type = map(string)
  default = {
    "application" = "minimal_api"
    "env"         = "prd"
  }
}
