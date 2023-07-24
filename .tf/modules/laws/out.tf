# Type: terraform output

output "log_analytics_workspace_id" {
  value = azurerm_log_analytics_workspace.laws-app.id
}
