# How to login
``` bash
ssh ('username')@butrosgroot.com -p ('port of the server')
```
Fill in the password and you are in!

# How to use the server
## python virtual environment
``` bash
source /home/('username')/NatureTecht_env/bin/activate
```

## How to reload the static files
### go to direcotry
``` bash
cd NatureTech
```

### Run the next command
``` bash
python manage.py collectstatic --noinput
```

## How to restart uwsgi webserver (the server that runs the syncornes django app)
``` bash
sudo systemctl reload uwsgi-NatureTech.service
```

## How to restart daphne webserver (the server that runs the asyncornes django app)
``` bash
sudo systemctl reload daphne-NatureTech.service
```