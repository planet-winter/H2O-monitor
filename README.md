# H2O-monitor

A Python script for a Raspberry Pi running Raspian counting the waterflow 
of 9 valves with reed pulse switches.

Reports readings to a DB (postgres) and visualizes them with a Grafana Dashboard


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
createuser h2o -P --interactive

Shall the new role be a superuser? (y/n) n
Shall the new role be allowed to create databases? (y/n) y
Shall the new role be allowed to create more new roles? (y/n) n
```

install grafana visualization
```
sudo apt-get install -y adduser libfontconfig
wget https://s3-us-west-2.amazonaws.com/grafana-releases/release/grafana_5.4.0_armhf.deb
sudo dpkg -i grafana_5.4.0_armhf.deb

sudo systemctl daemon-reload
sudo systemctl enable grafana-server
sudo systemctl start grafana-server
```

clone this repo 
```
TODO
cd repo
```

install requirements
```
sudo apt-get install python3-pip
sudo pip3 install --upgrade -r requirements.txt
TODO
```

autostart service 
```
TODO
sudo cp ./h2o-monitor.service /etc/systemd/system/
sudo systemd daemon-reload
sudo systemd enable h2o-monitor
sudo systemd start h2o-monitor
TODO
```
