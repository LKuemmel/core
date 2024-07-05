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

now = datetime.now()
current_time = now.strftime("%Y-%m-%d")

globvar_occp_client_start = False
globvar_occp_client_run = False
chargepoint_lst = []


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
        return transaction_id_resp[0]

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

    async def get_meter(self, meter_value_charged):
        meter = call.MeterValues(
            connector_id=2,
            transaction_id=11,
            meter_value=[{"timestamp": current_time,
                          "sampledValue": [
                              {
                                  "value": f'{meter_value_charged}',
                                  "context": "Sample.Periodic",
                                  "format": "Raw",
                                  "measurand": "Energy.Active.Import.Register",
                                  "location": "Outlet",
                                  "unit": "Wh"
                              },
                          ]}],
        )
        response_meter = await self.call(meter)
        print("response_meter: ", response_meter)


class OCPPClient(ChargePoint):
    _detected_chargepoints: list[ChargePoint] = []

    globvar_url: str

    def __init__(self) -> None:
        try:
            pass
        except Exception:
            log.exception("Fehler im OCPP-Modul")

    async def _keep_connection(meter_value_charged):
        try:
            # async for event in ChargePoint.async_read_loop():
            #    if event.type == "test"
            if globvar_occp_client_run is False:
                async with websockets.connect(
                    'ws://128.140.100.76:8080/steve/websocket/CentralSystemService/simtest1',
                    # url,
                    subprotocols=['ocpp1.6']
                ) as ws:
                    global cp
                    cp = ChargePoint('CP_1', ws)
                    print(type(cp))
                    await asyncio.gather(cp.start(), cp.send_boot_notification())

            if globvar_occp_client_run:
                try:
                    # for x in chargepoint_lst:
                    # await asyncio.gather(cp.get_meter(x))
                    await asyncio.gather(cp.get_meter(meter_value_charged))
                # await ws.wait_closed()
                except Exception as e:
                    print(e)
        except Exception:
            log.exception("Fehler im OCPP-Modul")

    def get_ocpp_config():
        return {
            "data": {
                "url": "",
            },
        }

    def get_config(occp_config):
        global globvar_url
        globvar_url = occp_config["data"]["url"]

    def get_url():
        global globvar_url
        return globvar_url

    def ocpp_test(cp):
        # Hier muss cp data übergeben werden an thread architektur und diese schiebt die anfragen raus
        # url = OCPPClient.get_url()
        global chargepoint_lst
        print(cp.num)
        if cp.data.get.charge_state:
            meter_value_charged = cp.data.get.imported
            chargepoint_name = cp.data.config.name
            print(chargepoint_name, meter_value_charged)
            # chargepoint_lst.append(cp.num)
            # chargepoint_lst.append(chargepoint_name)
            chargepoint_lst.append(meter_value_charged)
            print(chargepoint_lst)
            global globvar_occp_client_run
            globvar_occp_client_run = True
            try:
                pass
                # asyncio.run(OCPPClient._keep_connection(chargepoint_lst))
                # asyncio.get_event_loop().run_until_complete(OCPPClient._keep_connection(meter_value_charged))
                asyncio.run_coroutine_threadsafe(OCPPClient._keep_connection(meter_value_charged), loop)
            except Exception as e:
                print(e)
            log.debug("Send Meter Values to OCPP")
        else:
            log.debug("Neither plugging nor charging")

    def state_occp_client_start():
        global globvar_occp_client_start
        return globvar_occp_client_start

    def state_occp_client_run():
        global globvar_occp_client_run
        return globvar_occp_client_run

    def start_ocpp():
        global globvar_occp_client_start
        globvar_occp_client_start = True
        print(globvar_occp_client_start)

    def stop_ocpp():
        global globvar_occp_client_run
        globvar_occp_client_run = False
        print(globvar_occp_client_run)

    def run(self):
        global loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        asyncio.ensure_future(self._keep_connection())
        loop.run_forever()
