#!/bin/bash

# =============================================================================
# Azure Container Apps Setup Script
# =============================================================================
# This script helps you set up the required Azure resources for the
# autohealing deployment pipeline.
#
# Prerequisites:
# - Azure CLI installed (https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)
# - Logged in to Azure (az login)
# =============================================================================

set -e

# Configuration - Update these values
RESOURCE_GROUP="rg-autohealing-demo"
LOCATION="eastus"
CONTAINER_REGISTRY_NAME="acrautohealdemo$RANDOM"  # Must be globally unique
CONTAINER_APP_ENV_NAME="cae-autohealing-demo"
CONTAINER_APP_NAME="autohealing-demo"

echo "🚀 Setting up Azure resources for Autohealing Pipeline Demo"
echo "============================================================"

# Create Resource Group
echo "📦 Creating Resource Group: $RESOURCE_GROUP"
az group create \
    --name $RESOURCE_GROUP \
    --location $LOCATION

# Create Azure Container Registry
echo "📦 Creating Azure Container Registry: $CONTAINER_REGISTRY_NAME"
az acr create \
    --resource-group $RESOURCE_GROUP \
    --name $CONTAINER_REGISTRY_NAME \
    --sku Basic \
    --admin-enabled true

# Get ACR credentials
echo "🔑 Getting ACR credentials..."
ACR_LOGIN_SERVER=$(az acr show --name $CONTAINER_REGISTRY_NAME --query loginServer -o tsv)
ACR_USERNAME=$(az acr credential show --name $CONTAINER_REGISTRY_NAME --query username -o tsv)
ACR_PASSWORD=$(az acr credential show --name $CONTAINER_REGISTRY_NAME --query "passwords[0].value" -o tsv)

# Create Container Apps Environment
echo "📦 Creating Container Apps Environment: $CONTAINER_APP_ENV_NAME"
az containerapp env create \
    --name $CONTAINER_APP_ENV_NAME \
    --resource-group $RESOURCE_GROUP \
    --location $LOCATION

# Create a placeholder Container App (will be updated by CI/CD)
echo "📦 Creating Container App: $CONTAINER_APP_NAME"
az containerapp create \
    --name $CONTAINER_APP_NAME \
    --resource-group $RESOURCE_GROUP \
    --environment $CONTAINER_APP_ENV_NAME \
    --image mcr.microsoft.com/azuredocs/containerapps-helloworld:latest \
    --target-port 80 \
    --ingress external \
    --min-replicas 0 \
    --max-replicas 3

# Get the Container App URL
CONTAINER_APP_URL=$(az containerapp show \
    --name $CONTAINER_APP_NAME \
    --resource-group $RESOURCE_GROUP \
    --query "properties.configuration.ingress.fqdn" -o tsv)

# Create Service Principal for GitHub Actions
echo "🔑 Creating Service Principal for GitHub Actions..."
SUBSCRIPTION_ID=$(az account show --query id -o tsv)
# MSYS_NO_PATHCONV=1 prevents Git Bash on Windows from converting /subscriptions path
SP_OUTPUT=$(MSYS_NO_PATHCONV=1 az ad sp create-for-rbac \
    --name "sp-github-autohealing-demo" \
    --role contributor \
    --scopes "/subscriptions/$SUBSCRIPTION_ID/resourceGroups/$RESOURCE_GROUP")

# Format the output for GitHub Actions AZURE_CREDENTIALS secret
APP_ID=$(echo "$SP_OUTPUT" | grep -o '"appId": "[^"]*"' | cut -d'"' -f4)
PASSWORD=$(echo "$SP_OUTPUT" | grep -o '"password": "[^"]*"' | cut -d'"' -f4)
TENANT=$(echo "$SP_OUTPUT" | grep -o '"tenant": "[^"]*"' | cut -d'"' -f4)

AZURE_CREDENTIALS=$(cat <<EOF
{
  "clientId": "$APP_ID",
  "clientSecret": "$PASSWORD",
  "subscriptionId": "$SUBSCRIPTION_ID",
  "tenantId": "$TENANT"
}
EOF
)

echo ""
echo "============================================================"
echo "✅ Setup Complete!"
echo "============================================================"
echo ""
echo "📋 Add these secrets to your GitHub repository:"
echo "   (Settings → Secrets and variables → Actions → New repository secret)"
echo ""
echo "AZURE_CONTAINER_REGISTRY=$ACR_LOGIN_SERVER"
echo "REGISTRY_USERNAME=$ACR_USERNAME"
echo "REGISTRY_PASSWORD=$ACR_PASSWORD"
echo "AZURE_RESOURCE_GROUP=$RESOURCE_GROUP"
echo ""
echo "AZURE_CREDENTIALS (paste the entire JSON below):"
echo "$AZURE_CREDENTIALS"
echo ""
echo "============================================================"
echo "🌐 Your Container App URL (after first deployment):"
echo "   https://$CONTAINER_APP_URL"
echo "============================================================"
echo ""
echo "📝 Next Steps:"
echo "1. Add the secrets above to your GitHub repository"
echo "2. Push code to the main branch to trigger deployment"
echo "3. If deployment fails, an issue will be auto-created!"
echo ""
