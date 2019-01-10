# H2O-monitor

A Python script for a Raspberry Pi running Raspian counting the waterflow 
of valves with reed pulse switches.

Reports readings to a DB (postgres) and visualizes them with a Grafana Dashboard



![alt text](https://github.com/planet-winter/H2O-monitor/raw/master/grafana.png "Grafan Sources monitor")
![alt text](https://github.com/planet-winter/H2O-monitor/raw/master/reed_valve.jpg "valve with reed contact")


## project setup

on a raspberry pi with raspian


install database server
```
sudo apt-get install postgresql
sudo systemctl enable  postgresql
sudo systemctl start postgresql
```

configure database user h2o with password h2o
```
sudo su postgres
createdb h2o
createuser h2o -P --interactive

Shall the new role be a superuser? (y/n) n
Shall the new role be allowed to create databases? (y/n) y
Shall the new role be allowed to create more new roles? (y/n) n

exit
```

install grafana visualization
```
sudo apt-get install -y adduser libfontconfig
sudo wget https://s3-us-west-2.amazonaws.com/grafana-releases/release/grafana_5.4.0_armhf.deb
sudo dpkg -i grafana_5.4.0_armhf.deb
```

edit grafana config to run on port 80
sudo nano /etc/grafana/grafana.ini
```
http_port = 80
```

```
sudo setcap 'cap_net_bind_service=+ep' /usr/sbin/grafana-server

sudo systemctl daemon-reload
sudo systemctl enable grafana-server
sudo systemctl start grafana-server
```

clone this repo 
```
cd /opt
sudo apt-get install git
sudo git clone https://github.com/planet-winter/H2O-monitor.git
cd /opt/H2O-monitor
```

install requirements
```
sudo apt-get install python3-pip
sudo pip3 install --upgrade -r requirements.txt
```

Setup grafana dashboard.
* open the systems IP address or hostname in a browser
* log in with admin and password admin
* in a new dashboard settings tab enter the dashboard.json content

Setup grafana Postgres data source
* goto configureation > data souces
* choose PostgreSQL
* enter Host: localhost and h2o as credentials and db name


autostart service 
```
sudo cp ./h2o-monitor.service /etc/systemd/system/
sudo systemd daemon-reload
sudo systemd enable h2o-monitor
sudo systemd start h2o-monitor
```



## Web Overview

open the systems IP address or hostname in a browser
