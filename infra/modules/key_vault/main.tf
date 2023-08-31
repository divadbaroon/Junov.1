
data "azurerm_client_config" "current" {}

resource "azurerm_key_vault" "key_vault" {
  name                        = var.key_vault_name
  location                    = var.location
  resource_group_name         = var.resource_group_name
  enabled_for_disk_encryption = true
  tenant_id                   = data.azurerm_client_config.current.tenant_id
  sku_name                    = "standard"

  access_policy {
    tenant_id = data.azurerm_client_config.current.tenant_id
    object_id = data.azurerm_client_config.current.object_id 

    key_permissions = [
      "Create",
      "Get",
      "List",
    ]

    secret_permissions = [
      "Set",
      "Get",
      "Delete",
      "Purge",
      "Recover",
      "List",
    ]
  }
}

resource "azurerm_key_vault_secret" "cognitive_services_key" {
  name         = "COGNITIVE-SERVICES-API-KEY"
  value        = var.cognitive_services_key
  key_vault_id = azurerm_key_vault.key_vault.id
}

resource "azurerm_key_vault_secret" "translator_key" {
  name         = "TRANSLATOR-API-KEY"
  value        = var.translator_key
  key_vault_id = azurerm_key_vault.key_vault.id
}
