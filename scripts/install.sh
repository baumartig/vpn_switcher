#! /bin/bash

# copy the files
cp ../src/vpn_switcher.py /usr/bin/vpn_switcher 
chown root:root /usr/bin/vpn_switcher
chmod 777 /usr/bin/vpn_switcher

if [ ! -f /etc/vpn_switcher/vpn_switcher.config ]
then
	mkdir /etc/vpn_switcher
	cp ../config/vpn_switcher.config /etc/vpn_switcher/vpn_switcher.config
	chown root:root	/etc/vpn_switcher/vpn_switcher.config
	chmod 644 /etc/vpn_switcher/vpn_switcher.config
fi

cp vpn_switcher.starter /etc/init.d/vpn_switcher
chown root:root /etc/init.d/vpn_switcher
chmod 755 /etc/init.d/vpn_switcher

# populate the startup script
update-rc.d vpn_switcher defaults
