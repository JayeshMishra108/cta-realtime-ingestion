param($resourceGroup = "realtime-rg", $functionApp = "cta-ingestor-app")

# Install Azure CLI: https://learn.microsoft.com/en-us/cli/azure/install-azure-cli

az login
az group create --name $resourceGroup --location eastus
az storage account create --name "${functionApp}storage" --location eastus --resource-group $resourceGroup --sku Standard_LRS
az functionapp create --name $functionApp --resource-group $resourceGroup --storage-account "${functionApp}storage" --runtime python --runtime-version 3.9 --functions-version 4 --consumption-plan-location eastus

# Set environment variables
az functionapp config appsettings set --name $functionApp --resource-group $resourceGroup --settings "CTA_API_KEY=$env:CTA_API_KEY" "EVENT_HUB_CONN_STR=$env:EVENT_HUB_CONN_STR"

# Deploy function
func azure functionapp publish $functionApp --python