#!/bin/bash
OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
RAMDISKDIR="${OPENWBBASEDIR}/ramdisk"
MODULEDIR=$(cd `dirname $0` && pwd)
#DMOD="EVU"
DMOD="MAIN"
Debug=$debug

#For development only
#Debug=1

if [ ${DMOD} == "MAIN" ]; then
	MYLOGFILE="${RAMDISKDIR}/openWB.log"
else
	MYLOGFILE="${RAMDISKDIR}/evu.log"
fi

bash "$OPENWBBASEDIR/packages/legacy_run.sh" "modules.victron.device" "counter" "${bezug_victronip}" "${bezug_id}" "${victron_energy_meter}">>${MYLOGFILE} 2>&1
ret=$?

openwbDebugLog ${DMOD} 2 "EVU RET: ${ret}"

wattbezug=$(<${RAMDISKDIR}/wattbezug)
echo $wattbezug