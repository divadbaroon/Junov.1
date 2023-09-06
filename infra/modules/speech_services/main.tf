
resource "azurerm_cognitive_account" "speech_service" {
  name                = var.speech_services_name
  location            = var.location
  resource_group_name = var.resource_group_name
  kind                = "SpeechServices"
  sku_name = "S0"
}
