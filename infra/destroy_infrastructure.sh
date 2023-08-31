#!/bin/bash

cd ./infrastructure

# Initialize Terraform and destroy the infra located within /modules
terraform init
terraform destroy
