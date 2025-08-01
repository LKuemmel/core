#!/usr/bin/env python3

import aiohttp
from asyncio import new_event_loop, set_event_loop
from typing import Union
from modules.vehicles.cupra import libcupra
from modules.vehicles.cupra.config import Cupra
from modules.vehicles.vwgroup.vwgroup import VwGroup


class api(VwGroup):

    def __init__(self, conf: Cupra, vehicle: int):
        super().__init__(conf, vehicle)

    # async method, called from sync fetch_soc, required because libvwid/libskoda/libcupra expect async environment
    async def _fetch_soc(self) -> Union[int, float, str]:
        async with aiohttp.ClientSession() as self.session:
            cupra = libcupra.cupra(self.session)
            return await super().request_data(cupra)


def fetch_soc(conf: Cupra, vehicle: int) -> Union[int, float, str]:

    # prepare and call async method
    loop = new_event_loop()
    set_event_loop(loop)

    # get soc, range from server
    a = api(conf, vehicle)
    soc, range, soc_ts, soc_tsX = loop.run_until_complete(a._fetch_soc())

    return soc, range, soc_ts, soc_tsX
