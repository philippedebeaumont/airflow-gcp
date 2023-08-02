terraform {
  required_version = ">=1.0"
  backend "local" {}
  required_providers {
    google = {
      source = "hashicorp/google"
    }
  }
}

locals {
  credentials_file = file(var.credentials)
  credentials = jsondecode(local.credentials_file)
  service_account_email = local.credentials.client_email
}

provider "google" {
  project = var.project
  region  = var.region
  zone    = var.zone
  credentials = local.credentials_file
}

resource "google_storage_bucket" "bucket" {
    name = "${var.bucket}_${var.project}"
    location = var.region
    force_destroy = true

    uniform_bucket_level_access = true

    lifecycle_rule {
      action {
        type = "Delete"
      }
      condition {
        age = 30
      }
    }
}

resource "google_bigquery_dataset" "dataset" {
  dataset_id                 = var.dataset
  project                    = var.project
  location                   = var.region
  delete_contents_on_destroy = true
}

resource "google_bigquery_table" "opensky-api-hourly-extraction" {
  dataset_id                  = google_bigquery_dataset.dataset.dataset_id
  table_id                    = var.table
  deletion_protection         = false

  labels = {
    env = "default"
  }

  schema = jsonencode({
    fields = [
      { name = "icao24", type = "STRING" },
      { name = "callsign", type = "STRING" },
      { name = "origin_country", type = "STRING" },
      { name = "time_position", type = "INT64" },
      { name = "last_contact", type = "INT64" },
      { name = "longitude", type = "FLOAT64" },
      { name = "latitude", type = "FLOAT64" },
      { name = "geo_altitude", type = "FLOAT64" },
      { name = "on_ground", type = "BOOL" },
      { name = "velocity", type = "FLOAT64" },
      { name = "true_track", type = "FLOAT64" },
      { name = "vertical_rate", type = "FLOAT64" },
      { name = "sensors", type = "STRING" },
      { name = "baro_altitude", type = "FLOAT64" },
      { name = "squawk", type = "STRING" },
      { name = "spi", type = "BOOL" },
      { name = "category", type = "INT64" },
    ]
  })

  depends_on = [google_bigquery_dataset.dataset]
}

resource "google_compute_firewall" "port_rules" {
  project     = var.project
  name        = "airflow-port"
  network     = var.network
  description = "Opens port 8080 for the airflow vm"

  allow {
    protocol = "tcp"
    ports    = ["8080"]
  }

  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["airflow"]
}

resource "google_compute_instance" "airflow_vm_instance" {
  name                      = "airflow-instance"
  machine_type              = "e2-standard-4"
  tags                      = ["airflow"]
  allow_stopping_for_update = true

  boot_disk {
    initialize_params {
      image = var.vm_image
      size  = 30
    }
  }

  network_interface {
    network = var.network
    access_config {
    }
  }

  service_account {
    email  = local.service_account_email
    scopes = [
      "https://www.googleapis.com/auth/cloud-platform",
      "https://www.googleapis.com/auth/bigquery",
      "https://www.googleapis.com/auth/devstorage.read_write",
      "https://www.googleapis.com/auth/compute.readonly",
    ]
  }

  metadata = {
    BUCKET_ID = google_storage_bucket.bucket.name
    DATASET_ID = var.dataset
    TABLE_ID = var.table
  }

  metadata_startup_script = file(var.airflow_setup)

  depends_on = [google_storage_bucket.bucket, google_compute_firewall.port_rules]
}