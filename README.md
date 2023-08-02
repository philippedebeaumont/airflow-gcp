This project aims to deploy an Airflow server on a GCP Compute Engine VM. It deploys the infrastructure with Terraform and the Airflow server run in a Docker container. Finally, it procs a dag hourly that extract plane data from the OpenSky API and store it in a Google Cloud Storage Bucket. It then load it into a BigQuery table. That project focuses on automatization to greatly facilitate the deployment of dags.

## Built with
- [![Terraform](https://img.shields.io/badge/Terraform-Cloud%20Deployment-7B42BC?logo=terraform)](https://www.terraform.io/)
- [![Docker](https://img.shields.io/badge/Docker-Contenerization-2496ED?logo=docker)](https://www.docker.com/)
- [![Airflow](https://img.shields.io/badge/Airflow-Scheduler-017CEE?logo=apacheairflow)](https://airflow.apache.org/)
- [![GCS](https://img.shields.io/badge/Cloud%20Storage-Datalake-4285F4)](https://cloud.google.com/storage)
- [![BigQuery](https://img.shields.io/badge/BigQuery-Data%20Warehouse-4285F4)](https://cloud.google.com/bigquery/)
- [![Compute Engine](https://img.shields.io/badge/Compute%20Engine-VM-4285F4)](https://cloud.google.com/compute/)

## Prerequisites
1. Install [**Terraform**](https://developer.hashicorp.com/terraform/downloads)
2. Create a Google Cloud Project. Export your service account credentials keys (should have compute engine permissions, gcs permissions, bigquery permissions). Enable Compute Engine API

## Installation

Clone the project:
```sh
git clone https://github.com/philippedebeaumont/airflow-gcp.git
cd airflow-gcp
```

Then you have to go into the terraform file to deploy the infrastructure on your google cloud project.
```sh
cd terraform
terraform init
```

```sh
terraform apply
```
You have to provide your google credentials file and your project id.

The dags are stored on the vm in the /airflow-gcp/airflow/dags folder if you want to add others. You'll have to manually adjust your cloud infrastructure to your new needs.

## Uninstallation
You have to destroy your cloud architecture with terraform to avoid unecessary billings. You'll have to provide the same informations that you entered when you created it.
```sh
terraform destroy
```
You have to provide the same informations you used when running the terraform apply.

You can also suppress your google cloud project.