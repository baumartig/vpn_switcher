#! /bin/bash

#stop the instance
killall vpn_switcher

# remove the file and folders
rm -f /usr/bin/vpn_switcher
rm -f /etc/init.d/vpn_switcher
