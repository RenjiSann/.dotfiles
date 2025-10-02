#! /bin/bash

DEVICES="$(bluetoothctl devices)"
COUNT="$(echo "$DEVICES" | wc -l)"

if [ "x$DEVICES" == "x" ]; then
	echo ""
	exit
fi
if [ "$COUNT" == "1" ]; then
	echo $(echo "$DEVICES" | cut -d' ' -f 1,2 --complement)
	exit
fi
echo "$COUNT devices"
