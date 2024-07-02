#!/usr/bin/env python3
import asyncio
from ocpp.v201.enums import RegistrationStatusType
import websockets
from ocpp.v16 import call
from ocpp.v16 import ChargePoint as cp
from datetime import datetime
import re
import logging
log = logging.getLogger(__name__)


def get_ocpp_config():
    return {
        "data": {
            "url": "",
        },
    }


def get_config(occp_config):
    url = occp_config["data"]["url"]
    return url


now = datetime.now()
current_time = now.strftime("%Y-%m-%d")


class ChargePoint(cp):

    async def send_boot_notification(self):
        request = call.BootNotification(
            charge_point_model="openWB",
            charge_point_vendor="openwb"
        )
        response = await self.call(request)

        if response.status == RegistrationStatusType.accepted:
            print("Connected to central system.")

    async def send_heart_beat(self):
        heartbeat = call.Heartbeat(

        )
        response_heartbeat = await self.call(heartbeat)
        print("Heartbeat: ", response_heartbeat)

    async def start_transaction(self):
        strtT = call.StartTransaction(connector_id=2,
                                      id_tag="user1",
                                      meter_start=0,
                                      timestamp=current_time
                                      )
        response_strtT = await self.call(strtT)
        print("response_strtT: ", response_strtT)
        transaction_str = str(response_strtT)[slice(str(response_strtT).index(("id_tag")))]
        transaction_id_resp = list(map(int, re.findall(r'\d+', transaction_str)))
        print("str:", transaction_id_resp[0])

    async def stop_transaction(self):
        strtT = call.StartTransaction(connector_id=2,
                                      id_tag="user1",
                                      meter_start=0,
                                      timestamp=current_time
                                      )
        response_strtT = await self.call(strtT)
        print("response_strtT: ", response_strtT)
        transaction_str = str(response_strtT)[slice(str(response_strtT).index(("id_tag")))]
        transaction_id_resp = list(map(int, re.findall(r'\d+', transaction_str)))
        print("str:", transaction_id_resp)
        stpT = call.StopTransaction(meter_stop=20,
                                    timestamp=current_time,
                                    transaction_id=transaction_id_resp[0],
                                    reason="Other",
                                    id_tag="user1"
                                    )
        response_stpT = await self.call(stpT)
        print("response_stpT: ", response_stpT)

    async def get_meter(self):
        meter = call.MeterValues(
            connector_id=2,
            transaction_id=11,
            meter_value=[{"timestamp": current_time,
                          "sampledValue": [
                              {
                                  "value": "0",
                                  "context": "Sample.Periodic",
                                  "format": "Raw",
                                  "measurand": "Energy.Active.Import.Register",
                                  "location": "Outlet",
                                  "unit": "Wh"
                              },
                              {
                                  "value": "50000.0",
                                  "context": "Sample.Periodic",
                                  "format": "Raw",
                                  "measurand": "Power.Active.Import",
                                  "location": "Outlet",
                                  "unit": "W"
                              },
                              {
                                  "value": "50.0",
                                  "context": "Sample.Periodic",
                                  "format": "Raw",
                                  "measurand": "Current.Import",
                                  "location": "Outlet",
                                  "unit": "A"
                              },
                              {
                                  "value": "63.0",
                                  "context": "Sample.Periodic",
                                  "format": "Raw",
                                  "measurand": "SoC",
                                  "location": "EV",
                                  "unit": "Percent"
                              },
                              {
                                  "value": "298.8",
                                  "context": "Sample.Periodic",
                                  "format": "Raw",
                                  "measurand": "Temperature",
                                  "location": "Body",
                                  "unit": "K"
                              },
                              {
                                  "value": "270.4",
                                  "context": "Sample.Periodic",
                                  "format": "Raw",
                                  "measurand": "Voltage",
                                  "location": "Inlet",
                                  "unit": "V"
                              },
                              {
                                  "value": "60",
                                  "context": "Sample.Periodic",
                                  "format": "Raw",
                                  "measurand": "Frequency",
                                  "location": "Inlet",
                              },
                          ]}],
        )
        response_meter = await self.call(meter)
        print("response_meter: ", response_meter)


class OCPPClient(ChargePoint):
    _detect_chargepoints: list[ChargePoint] = []

    def __init__(self) -> None:
        try:
            pass
        except Exception:
            log.exception("Fehler im OCPP-Modul")

    def start_ocpp_client(self) -> bool:
        return False
        # return len(self._detect_OCPP) > 0

    def start_ocpp():
        try:
            asyncio.run(main())
        except AttributeError:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(main())
            loop.close()

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        for chargepoint in self._detected_chargepoints:
            asyncio.ensure_future(self._read_events(chargepoint))
        loop.run_forever()


async def main():
    async with websockets.connect(
            'ws://128.140.100.76:8080/steve/websocket/CentralSystemService/simtest1',
            # url,
            subprotocols=['ocpp1.6']
    ) as ws:
        cp = ChargePoint('CP_1', ws)

        await asyncio.gather(cp.start(), cp.send_boot_notification(), cp.send_heart_beat(),
                             cp.start_transaction(), cp.get_meter(), cp.stop_transaction())
        await ws.wait_closed()
