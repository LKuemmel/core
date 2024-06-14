#!/usr/bin/env python3
from enum import Enum
import logging
import socket

from modules.common.abstract_device import DeviceDescriptor
from modules.common.component_state import RcrState
from modules.common.configurable_io import ConfigurableIo
from modules.common.modbus import ModbusTcpClient_
from modules.common.version_by_telnet import get_version_by_telnet
from modules.io import actions
from modules.io.devices.dimm_kit.config import IoLan

log = logging.getLogger(__name__)


class State(Enum):
    OPENED = False
    CLOSED = True


VALID_VERSIONS = ["openWB DimmModul"]


def create_io(config: IoLan):
    def updater():
        if version:
            input_1 = State(client.read_coils(0x0000, 1, unit=config.configuration.modbus_id))
            input_2 = State(client.read_coils(0x0001, 1, unit=config.configuration.modbus_id))
            [getattr(actions, config.actions[f"input_{i}"]["action"])(getattr(__name__, f"input_{i}"),
                                                                      config.actions[f"input_{i}"]["action_parameters"]) for i in range(1, 11)]
    try:
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
        except (ConnectionRefusedError, ValueError) as e:
            e.args += (("Firmware des openWB Dimm-& Control-Kit ist nicht mit openWB software2 kompatibel. "
                        "Bitte den Support kontaktieren."),)
            raise e
        except socket.timeout as e:
            e.args += (("Die IP-Adresse ist nicht erreichbar. Bitte den Support kontaktieren."),)
            raise e
    except Exception:
        log.exception("Fehler in create_device")
    return ConfigurableIo(config=config, component_updater=updater)


device_descriptor = DeviceDescriptor(configuration_factory=IoLan)
