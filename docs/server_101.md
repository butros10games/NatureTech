# How to login
``` bash
ssh ('username')@butrosgroot.com -p ('port of the server')
```
Fill in the password and you are in!

# How to use the server
## python virtual environment
``` bash
source /home/('username')/NatureTech_env/bin/activate
```

## How to reload the static files
### go to direcotry
``` bash
cd NatureTech
```

### Run the next command      CSS, images and JS changes
``` bash
python manage.py collectstatic_npm --noinput
```

## How to restart uwsgi webserver (the server that runs the syncornes django app)      HTML and Django changes
``` bash
sudo systemctl reload uwsgi-NatureTech.service
```

## How to restart daphne webserver (the server that runs the asyncornes django app) 
``` bash
sudo systemctl reload daphne-NatureTech.service
```