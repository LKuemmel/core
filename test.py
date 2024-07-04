import asyncio

from ocpp.v201.enums import RegistrationStatusType
import logging
import websockets
from ocpp.v16.enums import Action
from ocpp.routing import on
from ocpp.v16 import call
from ocpp.v16 import ChargePoint as cp
from datetime import datetime
import re

meterlist = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

logging.basicConfig(level=logging.DEBUG)
now = datetime.now()
# date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
current_time = now.strftime("%Y-%m-%d")
print(current_time)


class ChargePoint(cp):

    @on(Action.BootNotification)
    async def send_boot_notification(self):
        request = call.BootNotification(
            charge_point_model="openWB",
            charge_point_vendor="openwb"
        )
        response = await self.call(request)

        if response.status == RegistrationStatusType.accepted:
            print("Connected to central system.")

    @ on(Action.Heartbeat)
    async def send_heart_beat(self):
        heartbeat = call.Heartbeat(
            current_time=datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S') + "Z"
        )
        response_heartbeat = await self.call(heartbeat)
        print("Heartbeat: ", response_heartbeat)
        return heartbeat

    @on(Action.StartTransaction)
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

    @on(Action.StopTransaction)
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

    @on(Action.RemoteStartTransaction)
    async def on_remote_start_transaction(self, **kwargs):
        request = call.RemoteStartTransactionPayload(**kwargs)
        logging.debug(f"(Charging Station) {self.id=} <- {request=}")
        response = call.RemoteStartTransactionPayload(
            # status=Action.RemoteStartStopStatus.accepted.value
        )
        logging.debug(f"(Charging Station) {self.id=} -> {response=}")
        return response

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

    # to authorize the charging session, the charger sends the Authorize Request (ID-Tag needs to be valid in ocpp backend)
    async def authorize(self):
        auth = call.Authorize(
            id_tag="user1"
        )
        response_auth = await self.call(auth)
        print("response_auth: ", response_auth)

    async def status_notification(self):
        stat = call.StatusNotification(
            connector_id=2,
            error_code="NoError",
            status="Available",
            timestamp=current_time
        )
        response_stat = await self.call(stat)
        print("response_stat: ", response_stat)

    # getCompositeSchedule request to get the maximum power before any other profiles are set
    async def get_composite_schedule(self):
        gcs = call.GetCompositeSchedule(
            connector_id=2,
            duration=5,
            charging_rate_unit="A"
        )
        response_gcs = await self.call(gcs)
        print("response_gcs: ", response_gcs)

    # setChargingProfile sequence in order to start charging if car is connected
    @ on(Action.SetChargingProfile)
    async def set_charging_profile(self, connector_id):
        scp = call.SetChargingProfile(
            connector_id=connector_id,
            cs_charging_profiles={"chargingProfileId": 1,
                                  "chargingProfileKind": "Absolute",
                                  "chargingProfilePurpose": "TxProfile",
                                  "chargingSchedule": {
                                      "chargingRateUnit": "W",
                                      "chargingSchedulePeriod": [{
                                          "limit": 11000,
                                          "startPeriod": 0,
                                      }, {
                                          "limit": 9000,
                                          "startPeriod": 780,
                                      }, {
                                          "limit": 4500,
                                          "startPeriod": 1680,
                                      },

                                      ], "duration": 86400,
                                  },
                                  "stackLevel": 16,
                                  "transactionId": 11,
                                  "validFrom": "2024-06-01 00:00",
                                  "validTo": "2028-08-31 00:00"}
        )
        response_scp = await self.call(scp)
        print("response_scp: ", response_scp)


async def main():
    async with websockets.connect(
            'ws://128.140.100.76:8080/steve/websocket/CentralSystemService/simtest1',
            subprotocols=['ocpp1.6']
    ) as ws:
        cp = ChargePoint('CP_1', ws)

        asyncio.gather(cp.start(), cp.send_boot_notification())
        # global meterlist
        for x in meterlist:
            asyncio.gather(cp.get_meter(x))

            # await asyncio.gather(cp.start(), cp.send_boot_notification())
            # await asyncio.gather(cp.start(), cp.send_boot_notification(), cp.authorize(), cp.status_notification(), cp.start_transaction(),
            #                    cp.get_composite_schedule(), cp.set_charging_profile(2))
            # await asyncio.gather(cp.start(), cp.send_boot_notification(), cp.authorize(), cp.send_heart_beat())

            # await asyncio.gather(cp.start(), cp.send_boot_notification(), cp.status_notification(), cp.send_heart_beat())

        await ws.wait_closed()


if __name__ == '__main__':
    # loop = asyncio.get_event_loop()
    # asyncio.ensure_future(main())
    # asyncio.ensure_future(actions())
    # loop.run_until_complete(main())
    # loop.run_forever()

    try:
        # asyncio.run() is used when running this example with Python 3.7 and
        # higher.
        asyncio.run(main())
    except AttributeError:
        # For Python 3.6 a bit more code is required to run the main() task on
        # an event loop.
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
        loop.close()
