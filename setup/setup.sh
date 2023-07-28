sudo apt-get install pip
sudo apt-get install git
sudo apt-get install python3-venv
sudo apt-get install -y supervisor
git clone https://github.com/philippedebeaumont/airflow-gcp.git
cd airflow-gcp
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
airflow db init
cd ..
mkdir airflow/dags
cp airflow-gcp/api_call_to_gcs.py airflow/dags/
sudo mkdir -p /var/log/airflow
export USERNAME=$(whoami)
sudo cp airflow-gcp/airflow.conf /etc/supervisor/conf.d/
sudo nano airflow/.env

airflow users create \
  --username airflow1 \
  --firstname YourFirstName \
  --lastname YourLastName \
  --email your_email@example.com \
  --role Admin \
  --password airflow1


sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start airflow-webserver
sudo supervisorctl start airflow-scheduler