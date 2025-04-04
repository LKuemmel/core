#!/usr/bin/env python3
from typing import Dict, Union

from dataclass_utils import dataclass_from_dict
from modules.common.abstract_device import AbstractBat
from modules.common.component_state import BatState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo, FaultState
from modules.common.modbus import ModbusDataType, ModbusTcpClient_
from modules.common.simcount import SimCounter
from modules.common.store import get_bat_value_store
from modules.devices.ampere.ampere.config import AmpereBatSetup


class AmpereBat(AbstractBat):
    def __init__(self,
                 device_id: int,
                 component_config: Union[Dict, AmpereBatSetup],
                 modbus_id: int) -> None:
        self.__device_id = device_id
        self.component_config = dataclass_from_dict(AmpereBatSetup, component_config)
        self.modbus_id = modbus_id
        self.sim_counter = SimCounter(self.__device_id, self.component_config.id, prefix="speicher")
        self.store = get_bat_value_store(self.component_config.id)
        self.fault_state = FaultState(ComponentInfo.from_component_config(self.component_config))

    def update(self, client: ModbusTcpClient_) -> None:
        power = client.read_input_registers(535, ModbusDataType.INT_16, unit=self.modbus_id) * -1
        soc = client.read_input_registers(1339, ModbusDataType.UINT_16, unit=self.modbus_id)

        imported, exported = self.sim_counter.sim_count(power)
        bat_state = BatState(
            power=power,
            soc=soc,
            imported=imported,
            exported=exported
        )
        self.store.set(bat_state)


component_descriptor = ComponentDescriptor(configuration_factory=AmpereBatSetup)
