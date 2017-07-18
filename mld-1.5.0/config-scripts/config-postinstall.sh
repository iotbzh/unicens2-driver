#!/bin/sh

# Enable automatic default config when mostconf is loaded
# Author: fulup/at/iot.bzh
# Date  : Avril 2017
# Object: Install udev and modprobe rules after driver install

BASEDIR=`dirname $0`

echo "*** Post install modeprobe & udev rules"
cp $BASEDIR/45-mostnet.conf /etc/modprobe.d/
cp $BASEDIR/45-mostnet.rules /etc/udev/rules.d/
udevadm control --reload-rules
