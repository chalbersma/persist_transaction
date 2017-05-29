# Setup Notes

## Setup 

* Setup User for Persistent Transactions (percy)

	sudo useradd -m -r -s /sbin/nologin -d /var/percy -m -c "User for Persistent Transactions" percy
	
* Make Code Locationa and Setup

	sudo mkdir -p /opt
	
* Get Code (But as root so percy can't change it)

	sudo git clone https://github.com/chalbersma/persist_transaction.git
	
* Install Electrum and Mysql

	sudo apt install mariadb-server mariadb-client python3 python-qt4 python-pip python-slowaes python3-pip python3-virtualenv python-virtualenv apache2 ssl-cert logrotate python3-pymysql
	
	* Be Sure to Setup a Mariadb Root Password
	
* Enable MySQL

	sudo systemctl status mysql
	sudo systemctl enable mysql
	
* Install Electrum Daemon (use the latest from the [downloads](https://electrum.org/#download) site.

	su -s /bin/bash - percy
	virtualenv -p python2 electrum
	cd /var/percy/electrum
	source bin/activate
	pip install https://download.electrum.org/2.8.2/Electrum-2.8.2.tar.gz
	
* Enable Electrum as a Daemon

	sudo su -s /bin/bash - percy
	cd /var/percy/electrum
	source bin/activate
	electrum create
	# Enter Password But never use this wallet for funds!
	electrum daemon start # Test daemon starts
	electrum daemon stop # Test Daemon stop
	
* Install Unit File

	sudo cp /opt/persist_transaction/setup/electrum.service /lib/systemd/system/
	sudo systemctl enable electrum.service
	sudo systemctl start electrum.service
	
* Setup MariaDB Schema & User

	* Run the commands in `setup.sql`. Be sure to change the `persist@localhost` password to a random one of your choice.

* Setup the config file for persistent_transactions change `config.ini` be sure to set the database password

	sudo cp /opt/persist_transaction/config.ini.sample /opt/persist_transaction/config.ini
	sudo vim /opt/persist_transaction/config.ini
	
* Create the VirtualEnv for Python3
	
	su - 
	virtualenv -p python3 /opt/persist_transaction
	source /opt/persist_transaction/bin/activate
	pip3 install flask flask_cors pymysql requests
	
* Add an alias to `/opt/persist_transaction/bin/activate` (Preferably at the end of the file)

	alias electrum="/var/percy/electrum/bin/electrum"
	
* *Optional* Test that it works

	sudo su -s /bin/bash - percy
	source /opt/persist_transaction/bin/activate
	electrum daemon status
	
* Install Persistent Transaction Service
	
	sudo cp /opt/persist_transaction/setup/persist_transaction.service /lib/systemd/system/
	sudo systemctl enable persist_transaction.service
	sudo systemctl start persist_transaction.service

* Install Process Transaction Crontab Job

	sudo cp /opt/persist_transaction/setup/cron.d/process_transaction /etc/cron.d/
	sudo mkdir /var/log/percy
	sudo chown percy.percy /var/log/percy
	
* Install Log File Rotate Script

	sudo cp /opt/persist_transaction/setup/logrotate.d/persist_transaction.conf /etc/logrotate.d/persist_transaction.conf

* Install Apache For Forwarding

	* Pre Work
	
		sudo a2dissite 000-default
		sudo a2enmod ssl
		sudo a2enmod headers
		sudo a2enmod proxy
		sudo a2enmod proxy_http
		
	* Add Our Flask Redirect 
	
		sudo cp /opt/persist_transaction/setup/percy_flask.conf /etc/apache2/sites-available/
		sudo a2ensite percy_flask
		sudo systemctl restart apache2
		
	* Right now the system is listening on a self signed certificate. You should use something like [let's encrypt](https://letsencrypt.org/) if you want your service to be publicly available.
	
	* Optionally you can put in an apache http->https redirect or you can use the redirect example page in `/opt/persist_transaction/setup/index.html` to redirect to the proper place. (Please note that you'll need to change the hostname).
