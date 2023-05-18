# log analytics workspace
resource "azurerm_log_analytics_workspace" "laws-app" {
  name                = var.app_name
  location            = var.location
  resource_group_name = var.resource_group_name
  sku                 = "PerGB2018"
  retention_in_days   = 30
  tags                = var.tags
}

# container insights
resource "azurerm_log_analytics_solution" "laws_continsights" {
  solution_name         = "ContainerInsights"
  location              = var.location
  resource_group_name   = var.resource_group_name
  workspace_resource_id = azurerm_log_analytics_workspace.laws-app.id
  workspace_name        = azurerm_log_analytics_workspace.laws-app.name
  plan {
    publisher = "Microsoft"
    product   = "OMSGallery/ContainerInsights"
  }
}
