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
	`deletestring` VARCHAR(64) NOT NULL default "none",
	PRIMARY KEY (`id`)
);

; Alter for Confirm String
; alter table `trked_trans` add deletestring VARCHAR(64) NOT NULL DEFAULT "none";

CREATE TABLE `attempts` (
	`atid` INT UNSIGNED NOT NULL AUTO_INCREMENT,
	`fk_trked_trans_id` INT UNSIGNED NOT NULL REFERENCES trked_trans(id),
	`checkdate` TIMESTAMP NOT NULL default CURRENT_TIMESTAMP,
	`result` ENUM('resubmit', 'invalid', 'confirmed', 'retirement'), 
	PRIMARY KEY (`atid`)
);

; Alter for `attempts`
; alter table `attempts` MODIFY COLUMN `result` ENUM('resubmit', 'invalid', 'confirmed', 'retirement') ; 

CREATE TABLE `emails` (
	`emailid` INT UNSIGNED NOT NULL AUTO_INCREMENT,
	`email` VARCHAR(64) NOT NULL UNIQUE,
	`confirmstring` VARCHAR(64),
	`active` BOOLEAN NOT NULL,
	PRIMARY KEY (`emailid`)
);

CREATE TABLE `notify_lookup` (
	`notifyid` INT UNSIGNED NOT NULL AUTO_INCREMENT,
	`fk_trked_trans_id` INT UNSIGNED NOT NULL REFERENCES trked_trans(id),
	`fk_emailid` INT UNSIGNED NOT NULL REFERENCES emails(emailid),
	PRIMARY KEY (`notifyid`)
);

create unique index notifyLookup_txemail on notify_lookup(fk_trked_trans_id, fk_emailid);

create user 'persist'@'localhost' identified by 'yerpassword';
grant insert, update, select, delete on longtrans.attempts to 'persist'@'localhost';
grant insert, update, select, delete on longtrans.trked_trans to 'persist'@'localhost';
grant insert, update, select, delete on longtrans.emails to 'persist'@'localhost';
grant insert, update, select, delete on longtrans.notify_lookup to 'persist'@'localhost';
