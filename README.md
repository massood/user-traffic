
# User Traffic

## Setup

```bash
sudo apt install python3-pip git
sudo python3 -m pip install virtualenv

git clone https://github.com/massood/user-traffic.git
cd user-traffic/

virtualenv --python=python3 venv
. venv/bin/activate
pip install -r requirements.txt
```

## Upgrading

```bash
cd user-traffic/
git pull
```

## Running

```bash
cd user-traffic/
. venv/bin/activate

./run.sh
```

You can access the site at: http://127.0.0.1:5000/

Replace 127.0.0.1 with the **server IP**. Also **open the port 5000** on firewall.
