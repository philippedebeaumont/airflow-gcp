#!/bin/bash

sudo apt update
sudo apt-get -y install docker.io
sudo groupadd docker
sudo gpasswd -a $USER docker
sudo service docker restart
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo apt-get install git
git clone https://github.com/philippedebeaumont/airflow-gcp.git
cd airflow-gcp/airflow
BUCKET_ID=$(curl -H "Metadata-Flavor: Google" "http://metadata/computeMetadata/v1/instance/attributes/BUCKET_ID")
DATASET_ID=$(curl -H "Metadata-Flavor: Google" "http://metadata/computeMetadata/v1/instance/attributes/DATASET_ID")
TABLE_ID=$(curl -H "Metadata-Flavor: Google" "http://metadata/computeMetadata/v1/instance/attributes/TABLE_ID")
echo "" | sudo tee -a .env
echo "BUCKET_ID=$BUCKET_ID" | sudo tee -a .env
echo "DATASET_ID=$DATASET_ID" | sudo tee -a .env
echo "TABLE_ID=$TABLE_ID" | sudo tee -a .env
sudo docker-compose up -d