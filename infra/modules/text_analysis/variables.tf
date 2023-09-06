
variable "resource_group_name" {
  type = string
  description = "The name of the resource group."
}
  
variable "text_analysis_name" {
  type = string
  description = "The name of the text analysis resource."
}

variable "location" {
  type = string
  description = "The location of the text analysis resource."
}