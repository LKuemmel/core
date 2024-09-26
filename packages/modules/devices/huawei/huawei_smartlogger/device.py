#!/usr/bin/env python3
import logging
from typing import Iterable, Union
from modules.common.abstract_device import DeviceDescriptor
from modules.common.component_context import SingleComponentUpdateContext
from modules.common import modbus
from modules.common.configurable_device import ComponentFactoryByType, ConfigurableDevice, MultiComponentUpdater
from modules.devices.huawei.huawei_smartlogger.bat import Huawei_SmartloggerBat
from modules.devices.huawei.huawei_smartlogger.config import Huawei_Smartlogger, Huawei_SmartloggerBatSetup
from modules.devices.huawei.huawei_smartlogger.config import (Huawei_SmartloggerCounterSetup,
                                                              Huawei_SmartloggerInverterSetup)
from modules.devices.huawei.huawei_smartlogger.counter import Huawei_SmartloggerCounter
from modules.devices.huawei.huawei_smartlogger.inverter import Huawei_SmartloggerInverter


log = logging.getLogger(__name__)


huawei_smartlogger_component_classes = Union[Huawei_SmartloggerBat,
                                             Huawei_SmartloggerCounter,
                                             Huawei_SmartloggerInverter]


def create_device(device_config: Huawei_Smartlogger):
    def create_bat_component(component_config: Huawei_SmartloggerBatSetup):
        return Huawei_SmartloggerBat(device_config.id, component_config, client)

    def create_counter_component(component_config: Huawei_SmartloggerCounterSetup):
        return Huawei_SmartloggerCounter(device_config.id, component_config, client)

    def create_inverter_component(component_config: Huawei_SmartloggerInverterSetup):
        return Huawei_SmartloggerInverter(device_config.id, component_config, client)

    def update_components(components: Iterable[Union[Huawei_SmartloggerBat,
                                                     Huawei_SmartloggerCounter,
                                                     Huawei_SmartloggerInverter]]):
        with client:
            for component in components:
                with SingleComponentUpdateContext(component.fault_state):
                    component.update()

    try:
        client = modbus.ModbusTcpClient_(device_config.configuration.ip_address, device_config.configuration.port)
        client.connect()
    except Exception:
        log.exception("Fehler in create_device")
    return ConfigurableDevice(
        device_config=device_config,
        component_factory=ComponentFactoryByType(
            bat=create_bat_component,
            counter=create_counter_component,
            inverter=create_inverter_component,
        ),
        component_updater=MultiComponentUpdater(update_components)
    )


device_descriptor = DeviceDescriptor(configuration_factory=Huawei_Smartlogger)
