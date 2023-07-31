variable "project" {
  description = "Your GCP Project ID"
  type        = string
}

variable "credentials" {
  description = "Your google credentials"
  type        = string
}

variable "bucket" {
  description = "Your bucket name"
  default = "datalake"
  type        = string
}

variable "region" {
  description = "Your project region"
  default = "europe-west9"
  type        = string
}

variable "zone" {
  description = "Your project zone"
  default = "europe-west9-a"
  type        = string
}

variable "dataset" {
  description = "Your dataset name."
  default = "opensky_data"
  type        = string
}

variable "table" {
  description = "Your table name."
  default = "opensky-api-hourly-extraction"
  type        = string
}

variable "storage_class" {
  description = "Storage class type for your bucket"
  default     = "STANDARD"
  type        = string
}

variable "network" {
  description = "Network for your vm instance"
  default     = "default"
  type        = string
}

variable "airflow_setup" {
  description = "Path to the airflow vm setup file"
  default     = "../setup/setup.sh"
  type        = string
}

variable "vm_image" {
  description = "Image for you VM"
  default     = "debian-cloud/debian-11"
  type        = string
}

locals {
}