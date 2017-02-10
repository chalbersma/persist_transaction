# Setup Notes

## Setup 

* Setup User for Persistent Transactions (percy)

	sudo useradd -m -r -s /sbin/nologin -d /var/percy -m -c "User for Persistent Transactions" percy
	
* Make Code Locationa and Setup

	sudo mkdir -p /opt
	
* Get Code (But as root so percy can't change it)

	sudo git clone https://github.com/chalbersma/persist_transaction.git
	
* Install Electrum and Mysql

	sudo apt install electrum mariadb-server mariadb-client python3
	
	* Be Sure to Setup a Mariadb Root Password
	
* Enable MySQL

	sudo systemctl status mysql
	sudo systemctl enable mysql
	
* Enable Electrum Daemon
