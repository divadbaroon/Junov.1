
resource "azurerm_cognitive_account" "TextAnalytics" {
  name                = var.text_analysis_name
  location            = var.location
  resource_group_name = var.resource_group_name
  kind                = "TextAnalytics"
  sku_name = "S"
}
