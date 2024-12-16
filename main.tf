terraform {
  required_providers {
    azurerm = {
      source = "hashicorp/azurerm"
      version = ">= 3.8"
    }
  }

  backend "azurerm" {
        resource_group_name  = "cohort32-33_ChiDin_ProjectExercise"
        storage_account_name = "devops24storageaccount"
        container_name       = "terraformcontainer"
        key                  = "terraform.tfstate"
    }
}

provider "azurerm" {
  features {}
  subscription_id = "d33b95c7-af3c-4247-9661-aa96d47fccc0"
}

data "azurerm_resource_group" "main" {
  name     = "cohort32-33_ChiDin_ProjectExercise"
}

resource "azurerm_service_plan" "main" {
  name                = "${var.prefix}-terraformed-asp"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  os_type             = "Linux"
  sku_name            = "B1"
}

resource "azurerm_linux_web_app" "main" {
  name                = "${var.prefix}-chiara-dinan-to-do-app"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  service_plan_id     = azurerm_service_plan.main.id

  site_config {
    application_stack {
      docker_image_name     = "chiaradinansoftwire/my-todo-app:latest"
      docker_registry_url   = "https://index.docker.io"
    }
  }

  app_settings = {
    FLASK_APP = "todo_app/app"
    FLASK_DEBUG = "false"
    SECRET_KEY = "secret-key"
    MONGODB_CONNECTION_STRING = azurerm_cosmosdb_account.main.primary_mongodb_connection_string
    MONGODB_DB_NAME = "${var.prefix}-chidin-todo-cosmos-db"
    MONGODB_COLLECTION_NAME = "to_do"
    WEBSITES_PORT = "5000"
    OAUTH_CLIENT_ID = "${var.OAUTH_CLIENT_ID}"
    OAUTH_CLIENT_SECRET = "${var.OAUTH_CLIENT_SECRET}"
  }
}

resource "azurerm_cosmosdb_account" "main" {
  name                = "${var.prefix}-chidin-todo-cosmos-db"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  offer_type          = "Standard"
  kind                = "MongoDB"

  capabilities {
    name = "MongoDBv3.4"
  }

  capabilities {
    name = "EnableMongo"
  }

  capabilities {
    name = "EnableServerless"
  }

  consistency_policy {
    consistency_level       = "Eventual"
  }

  geo_location {
    location          = "uksouth"
    failover_priority = 0
  }

  # lifecycle {
  #   prevent_destroy = true
  # }
}