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
echo "" | sudo tee -a .env
echo "BUCKET_ID=$BUCKET_ID" | sudo tee -a .env
echo "DATASET_ID=$DATASET_ID" | sudo tee -a .env
echo "TABLE_ID=$TABLE_ID" | sudo tee -a .env
sudo docker-compose up -d