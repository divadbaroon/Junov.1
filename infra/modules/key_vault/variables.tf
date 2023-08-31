
variable "resource_group_name" {
  type = string
  description = "The name of the resource group."
}
  
variable "key_vault_name" {
  type = string
  description = "The name of the key vault."
}

variable "location" {
  type = string
  description = "The location of the key vault."
}

variable "cognitive_services_key" {
  description = "The Cognitive Services Key"
  type        = string
}

variable "translator_key" {
  description = "The Translator Key"
  type        = string
}
