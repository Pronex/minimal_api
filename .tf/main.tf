# terraform main file

# main resource group
resource "azurerm_resource_group" "rg_app" {
  name     = var.rg_app
  location = var.default_location
  tags     = var.prd_tags
}

# log analytics workspace
module "log_analytics" {
  source              = "./modules/laws"
  app_name            = var.app_name
  location            = var.default_location
  resource_group_name = azurerm_resource_group.rg_app.name
  tags                = var.prd_tags
}

# app insights
module "appinsights" {
  source              = "./modules/appinsights"
  app_name            = var.app_name
  location            = var.default_location
  resource_group_name = azurerm_resource_group.rg_app.name
  application_type    = "web"
  tags                = var.prd_tags
}

# container app environment
resource "azurerm_container_app_environment" "cae-app" {
  name                       = "cae-${var.app_name}"
  location                   = var.default_location
  resource_group_name        = azurerm_resource_group.rg_app.name
  log_analytics_workspace_id = module.log_analytics.log_analytics_workspace_id
  tags                       = var.prd_tags
}

# user assigned identity
resource "azurerm_user_assigned_identity" "uai-app" {
  name                = "uai-${var.app_name}"
  location            = var.default_location
  resource_group_name = azurerm_resource_group.rg_app.name
  tags                = var.prd_tags
}

# role assignment
resource "azurerm_role_assignment" "ra-app" {
  scope                = data.azurerm_container_registry.acr_minimal_api.id
  role_definition_name = "AcrPull"
  principal_id         = azurerm_user_assigned_identity.uai-app.principal_id
  depends_on           = [azurerm_user_assigned_identity.uai-app]
}

# container app
resource "azurerm_container_app" "capp-app" {
  name                         = "capp-${var.app_name}"
  container_app_environment_id = azurerm_container_app_environment.cae-app.id
  resource_group_name          = azurerm_resource_group.rg_app.name
  revision_mode                = "Single"
  tags                         = var.prd_tags

  identity {
    type = "UserAssigned"
    identity_ids = [
      azurerm_user_assigned_identity.uai-app.id
    ]
  }

  ingress {
    external_enabled = true
    target_port      = 8080
    traffic_weight {
      latest_revision = true
      percentage      = 100
    }
  }

  registry {
    server   = data.azurerm_container_registry.acr_minimal_api.login_server
    identity = azurerm_user_assigned_identity.uai-app.id
  }

  template {
    container {
      name   = "minimal-api"
      image  = "${data.azurerm_container_registry.acr_minimal_api.login_server}/minimal-api:latest"
      cpu    = 0.25
      memory = "0.5Gi"

      env {
        name  = "APPINSIGHTS_INSTRUMENTATIONKEY"
        value = module.appinsights.appinsights_instrumentation_key
      }
      env {
        name  = "UNAME"
        value = var.uname
      }
      env {
        name  = "PWORD"
        value = var.pword
      }

      liveness_probe {
        port             = 8080
        transport        = "TCP"
        initial_delay    = 20
        interval_seconds = 20
      }
    }
    min_replicas = 1
    max_replicas = 10
  }

  depends_on = [azurerm_container_app_environment.cae-app]
}

# output

output "capp-name" {
  value = azurerm_container_app.capp-app.name
}

output "capp-ingress-fqdn" {
  value = azurerm_container_app.capp-app.ingress[0].fqdn
}
