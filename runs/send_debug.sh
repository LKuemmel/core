#!/bin/bash
OPENWBBASEDIR=$(cd "$(dirname "$0")/../" && pwd)
sleep 60

debugFile=${OPENWBBASEDIR}/ramdisk/debug.log
touch "$debugFile"
{
	echo "$1" > "$debugFile"
	debugemail=$2
	echo "############################ system ###############"
	uptime
	free
	echo "############################ storage ###############"
	df -h
	echo "############################ network ##############"
	ifconfig
	echo "############################ version ##############"
	cat "${OPENWBBASEDIR}/web/version"
	cat "${OPENWBBASEDIR}/web/lastcommit"
	echo "############################ main.log ##############"
	tail -2500 "${OPENWBBASEDIR}/ramdisk/main.log"
	echo "############################ mqtt ##############"
	tail -1000 "${OPENWBBASEDIR}/ramdisk/mqtt.log"

	for currentConfig in /etc/mosquitto/conf.d/99-bridge-*; do
		if [ -f "$currentConfig" ]; then
			echo "############################ mqtt bridge '$currentConfig' ######"
			sudo grep -F -v -e password "$currentConfig" | sed '/^#/ d'
		fi
	done

	echo "############################ mqtt topics ##############"
	timeout 1 mosquitto_sub -v -t 'openWB/#'

	# echo "############################ smarthome.log ##############"
	# tail -200 "${OPENWBBASEDIR}/ramdisk/smarthome.log"
} >> "$debugFile"

echo "***** uploading debuglog..." >> "$RAMDISKDIR/main.log"
curl --upload "$debugFile" "https://openwb.de/tools/debug2.php?debugemail=$debugemail"

echo "***** cleanup..." >> "$RAMDISKDIR/main.log"
rm "$debugFile"

echo "***** debuglog end" >> "$RAMDISKDIR/main.log"