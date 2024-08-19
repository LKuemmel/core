#!/usr/bin/env python3
from modules.io.devices.dimm_kit.config import IoLan
from modules.common.version_by_telnet import get_version_by_telnet
from modules.common.modbus import ModbusTcpClient_
from enum import Enum
import logging
import socket

from modules.common.abstract_device import DeviceDescriptor

log = logging.getLogger(__name__)


class State(Enum):
    OPENED = False
    CLOSED = True


VALID_VERSIONS = ["openWB DimmModul"]


def create_io(config: IoLan):
    def updater():
        return {0: State(client.read_coils(0x0000, 1, unit=config.configuration.modbus_id)),
                1: State(client.read_coils(0x0001, 1, unit=config.configuration.modbus_id))
                }

    version = False
    client = ModbusTcpClient_(config.configuration.ip_address, config.configuration.port)
    try:
        parsed_answer = get_version_by_telnet(VALID_VERSIONS[0], config.configuration.ip_address)
        for version in VALID_VERSIONS:
            if version in parsed_answer:
                version = True
                log.debug("Firmware des openWB Dimm-& Control-Kit ist mit openWB software2 kompatibel.")
            else:
                version = False
                raise ValueError
    except (ConnectionRefusedError, ValueError):
        log.exception("Dimm-Kit")
        raise Exception("Firmware des openWB Dimm-& Control-Kit ist nicht mit openWB software2 kompatibel. "
                        "Bitte den Support kontaktieren.")
    except socket.timeout:
        log.exception("Dimm-Kit")
        raise Exception("Die IP-Adresse ist nicht erreichbar. Bitte den Support kontaktieren.")
    return updater


device_descriptor = DeviceDescriptor(configuration_factory=IoLan)
