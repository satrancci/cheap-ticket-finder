python3 -m pip install --upgrade pip
python3 -m pip install --user virtualenv
python3 -m venv env
source env/bin/activate && python3 -m pip install -r requirements.txt
mkdir -p crawled_data/expedia
touch .env
# Then open .env and manually store:
# NORDVPN_USERNAME="<YOUR_USERNAME>"
# NORDVPN_PASSWORD="<YOUR_PASSWORD>"

docker build -t selenium .
docker pull bubuntux/nordvpn

