# Incident Notification Platform


## Description

- portal for the Notification Incident Platform;

## Ghetto dev installation

### container
```
lxc launch ubuntu:22.10 NISINP --storage your-storage
lxc exec NISINP -- /bin/bash 
```

### poetry

```
curl -sSL https://install.python-poetry.org | python3 -
```

at the end of the `~/.bashrc`
```
export PATH="/root/.local/bin:$PATH"
```

### postgres
```
apt get install postgres-14
sudo su postgres
psql
/password postgres 
# password
```

### NISINP
```
git clone https://github.com/informed-governance-project/NISINP.git
cd NISINP
git submodule update --recursive
poetry install
poetry build
poetry shell
poetry run python manage.py migrate
poetry run python manage.py manage.py createsuperuser
```

### js
```
git clone https://github.com/asdf-vm/asdf.git ~/.asdf --branch v0.12.0
```

at the end of the `~/.bashrc`
```
. "$HOME/.asdf/asdf.sh"
. "$HOME/.asdf/completions/asdf.bash"
```

```
asdf plugin add nodejs https://github.com/asdf-vm/asdf-nodejs.git
asdf install nodjs latest
asdf reshim nodejs
asdf global nodejs latest
```

```
cd NISINP
npm install
```

## lauch django app
```
poetry run python manage.py runserver 0.0.0.0:8000
```

## License

This software is licensed under
[GNU Affero General Public License version 3](https://www.gnu.org/licenses/agpl-3.0.html)
