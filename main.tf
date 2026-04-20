terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.6.0"
    }
  }
}

provider "google" {
  project = "zoomcamp-powerlifting" 
  region  = "us-west1"
}


resource "google_storage_bucket" "data-lake" {
  name          = "power-lifting-data-lake-2026" 
  location      = "US"
  force_destroy = true
}


resource "google_bigquery_dataset" "dataset" {
  dataset_id = "powerlifting_data"
  location   = "US"
}