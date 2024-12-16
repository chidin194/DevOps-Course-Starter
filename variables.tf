variable "prefix" {
  description = "The prefix used for all resources in this environment"
}

variable "OAUTH_CLIENT_ID" {
 type = string
 description = "OAuth client ID"
 sensitive = true
}

variable "OAUTH_CLIENT_SECRET" {
 type = string
 description = "OAuth client secret"
 sensitive = true
}