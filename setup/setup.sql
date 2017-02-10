; Create Database

create database longtrans;

use longtrans;

CREATE TABLE `trked_trans` (
	`id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
	`txid` VARCHAR(256) NOT NULL UNIQUE,
	`firstSeen` TIMESTAMP NOT NULL default CURRENT_TIMESTAMP,
	`lastchecked` TIMESTAMP NOT NULL default '0000-00-00 00:00:00' on UPDATE CURRENT_TIMESTAMP,
	`active` BOOLEAN NOT NULL,
	`hextx` TEXT NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE `attempts` (
	`atid` INT UNSIGNED NOT NULL AUTO_INCREMENT,
	`fk_trked_trans_id` INT NOT NULL REFERENCES trked_trans(id),
	`checkdate` TIMESTAMP NOT NULL default CURRENT_TIMESTAMP,
	`result` ENUM('resubmit', 'invalid', 'confirmed'), 
	PRIMARY KEY (`atid`)
);


create user 'persist'@'localhost' identified by 'yerpassword';
grant insert, update, select, delete on longtrans.attempts to 'persist'@'localhost';
grant insert, update, select, delete on longtrans.trked_trans to 'persist'@'localhost';
