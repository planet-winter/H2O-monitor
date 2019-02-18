# H2O-monitor

A Python script for a Raspberry Pi running Raspian counting the waterflow 
of valves with reed pulse switches.

Reports readings to a DB (InfluxDB) and visualizes them with a Grafana Dashboard



![alt text](https://github.com/planet-winter/H2O-monitor/raw/master/grafana.png "Grafan Sources monitor")
![alt text](https://github.com/planet-winter/H2O-monitor/raw/master/reed_valve.jpg "valve with reed contact")


## project setup

on a raspberry pi with raspian


install database server
```
echo "deb https://repos.influxdata.com/debian stretch stable" | sudo tee /etc/apt/sources.list.d/influxdb.list
sudo apt update
sudo apt install influxdb
sudo systemctl enable influxdb
sudo systemctl start influxdb

influx

CREATE DATABASE h2oflow

```

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
