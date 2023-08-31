#!/bin/bash

cd ./infrastructure

# Initialize Terraform and create the infras located within /modules
terraform init
terraform apply

