
output "key_vault_name" {
  value = azurerm_key_vault.key_vault.name
  description = "The name of the key vault."
}