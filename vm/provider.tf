terraform {
 required_providers {
  outscale = {
   source = "outscale/outscale"
   version = "0.12.0"
   }
 }
 backend "s3" {
 access_key = var.access_key4
 secret_key = var.secret_key
 region = "us-east-2"
 bucket = "devops-training-matteo"
 key = "terraform.tfstate"
 endpoint = "https://oos.us-east-2.outscale.com/"
 skip_region_validation = true
 skip_credentials_validation = true
  }
}


provider "outscale" {
  access_key_id  = var.access_key
  secret_key_id  = var.secret_key
  region         = "us-east-2"
}
