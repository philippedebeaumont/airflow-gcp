sudo apt-get install pip
sudo apt-get install git
sudo apt-get install python3-venv
git clone https://github.com/philippedebeaumont/airflow-gcp.git
cd airflow-gcp
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt