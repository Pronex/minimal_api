# Type: terraform output

output "appinsights_instrumentation_key" {
  value = azurerm_application_insights.appinsights.instrumentation_key
}
