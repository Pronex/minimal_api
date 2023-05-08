# variables
# base variables
variable "default_location" {
  type    = string
  default = "Westeurope"
}

variable "dev_rg" {
  type = string
}

variable "prd_rg" {
  type = string
}

# tags
variable "dev_tags" {
  type = map(string)
  default = {
    "application" = "minimal_api"
    "env"         = "dev"
  }
}

variable "prd_tags" {
  type = map(string)
  default = {
    "application" = "minimal_api"
    "env"         = "prd"
  }
}