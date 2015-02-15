#! /bin/bash

#stop the instance
/etc/init.d/vpn_switcher

# remove the file and folders
update-rc.d vpn_switcher remove
rm -f /usr/bin/vpn_switcher
rm -f /etc/init.d/vpn_switcher
