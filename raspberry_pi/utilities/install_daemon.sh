#!/bin/sh
# Installs the rashawk script to launch raspberry_pi as a deamon
# MUST BE ROOT OR USE SUDO!

chmod ugo+x ./rashawk.sh
cp ./rashawk.sh /etc/init.d
pushd ./
cd /etc/init.d
update-rc.d ./rashawk.sh defaults
popd

echo "Done.  Either restart the pi or sudo /etc/init.d/rashawk.sh start"
