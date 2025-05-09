from typing import List

import logging

from helpermodules.cli import run_using_positional_cli_args
from modules.common import store
from modules.common.abstract_device import DeviceDescriptor
from modules.common.abstract_vehicle import VehicleUpdateData
from modules.common.component_state import CarState
from modules.common.configurable_vehicle import ConfigurableVehicle
from modules.vehicles.leaf import api
from modules.vehicles.leaf.config import LeafSoc, LeafConfiguration


log = logging.getLogger(__name__)


def create_vehicle(vehicle_config: LeafSoc, vehicle: int):
    def updater(vehicle_update_data: VehicleUpdateData) -> CarState:
        return api.fetch_soc(
            vehicle_config.configuration.user_id,
            vehicle_config.configuration.password,
            vehicle_config.configuration.region,
            vehicle)
    return ConfigurableVehicle(vehicle_config=vehicle_config,
                               component_updater=updater,
                               vehicle=vehicle)


def leaf_update(user_id: str, password: str, region: str, charge_point: int):
    log.debug("leaf: user_id="+user_id+" region="+region+" charge_point="+str(charge_point))
    vehicle_config = LeafSoc(configuration=LeafConfiguration(charge_point,
                                                             user_id,
                                                             password,
                                                             region))
    store.get_car_value_store(charge_point).store.set(api.fetch_soc(
        vehicle_config.configuration.user_id,
        vehicle_config.configuration.password,
        vehicle_config.configuration.region,
        charge_point))


def main(argv: List[str]):
    run_using_positional_cli_args(leaf_update, argv)


device_descriptor = DeviceDescriptor(configuration_factory=LeafSoc)
