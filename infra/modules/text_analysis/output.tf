
output "text_analysis_key" {
  value = azurerm_cognitive_account.TextAnalytics.primary_access_key
}

output "text_analytics_endpoint" {
  value = azurerm_cognitive_account.TextAnalytics.endpoint
}
