#!/bin/bash

# Script's purpose: restart the omni* services
# Run this script as super user or using sudo
# Or... do this:
#    sudo chown root.root kick_omni.sh
#    sudo chmod 4755 kick_omni.sh
#
# Then every time you sudo ./kick_omni.sh, it should run fine.

/etc/init.d/omniorb-eventservice stop
/etc/init.d/omniorb4-nameserver stop
rm -f /var/lib/omniorb/*
rm -f /var/lib/omniEvents/*
/etc/init.d/omniorb4-nameserver start
/etc/init.d/omniorb-eventservice start
