locals {
  resource_group_name = "${var.project_name}-rg"
}

module "resource_group" {
  source = "../modules/resource_group"

  resource_group_name = local.resource_group_name
  resource_group_location = var.region
}

module "key_vault" {
  source = "../modules/key_vault"

  depends_on = [module.resource_group, 
                module.speech_services, 
                module.text_analysis, 
                module.translator]
  resource_group_name = local.resource_group_name
  key_vault_name = "${var.project_name}-vault"
  location = var.region

  cognitive_services_key = module.speech_services.speech_service_key
  translator_key         = module.translator.translator_key
  text_analysis_key = module.text_analysis.text_analysis_key
  text_analytics_endpoint = module.text_analysis.text_analytics_endpoint
}

output "key_vault_name_output" {
  value = module.key_vault.key_vault_name
}

module "speech_services" {
  source = "../modules/speech_services"

  depends_on = [module.resource_group]
  resource_group_name = local.resource_group_name
  speech_services_name = "${var.project_name}-speech-services"
  location = var.region
}

module "text_analysis" {
  source = "../modules/text_analysis"

  depends_on = [module.resource_group]
  resource_group_name = local.resource_group_name
  text_analysis_name = "${var.project_name}-text-analysis"
  location = var.region
}


module "translator" {
  source = "../modules/translator"

  depends_on = [module.resource_group]
  resource_group_name = local.resource_group_name
  translator_name = "${var.project_name}-translator"
  location = var.region
}
