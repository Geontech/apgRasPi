#!/bin/bash

# Script's purpose: restart the omni* services
# Run this script as super user or using sudo
# Or... do this:
#    sudo chown root.root kick_omni.sh
#    sudo chmod 4755 kick_omni.sh
#
# Then every time you sudo ./kick_omni.sh, it should run fine.

/sbin/service omniEvents stop
/sbin/service omniNames stop
rm -f /var/log/omniORB/*
rm -f /var/lib/omniEvents/*
/sbin/service omniNames start
/sbin/service omniEvents start
