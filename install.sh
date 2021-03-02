python3 -m pip install --upgrade pip
python3 -m pip install --user virtualenv
python3 -m venv env
source env/bin/activate && python3 -m pip install -r requirements.txt

docker build -t selenium .
docker pull bubuntux/nordvpn