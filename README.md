# Odoo 17

## Update src odoo

```shell
git submodule init
git submodule update
```

### Build odoo from source

- Requirement

[pyenv](https://github.com/pyenv/pyenv)
[nvm](https://github.com/nvm-sh/nvm)

- install odoo dependencies

```shell
sudo apt install postgresql postgresql-client
sudo ./src/setup/debinstall.sh
sudo npm install -g rtlcss
wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-3/wkhtmltox_0.12.6.1-3.jammy_amd64.deb -P /tmp
sudo apt install -y /tmp/wkhtmltox_0.12.6.1-3.jammy_amd64.deb
pip install inotify
```

### Run odoo

- run database, setup env and install requirements

```shell
docker-compose up -d
python -m venv venv
source ./venv/bin/activate
pip install -r src/requirements.txt
```

- run odoo

```shell
python src/odoo-bin --dev=all --log-web --log-sql -c odoo.conf
```

- create module

```shell
python src/odoo-bin scaffold player1 extra-addons -t default
```