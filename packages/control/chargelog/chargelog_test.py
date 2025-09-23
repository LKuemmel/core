
import datetime
import json
from unittest.mock import MagicMock, Mock, mock_open, patch

import pytest

from control import data
from control.chargelog import chargelog
from control.chargelog.chargelog import calculate_charged_energy_by_source
from control.chargepoint.chargepoint import Chargepoint
from control.chargepoint.chargepoint_data import empty_enery_source_dict_factory
from helpermodules import timecheck


def mock_daily_log_with_charging(date: str, num_of_intervalls, monkeypatch):
    """erzeugt ein daily_log, im ersten Eintrag gibt es keine Änderung, danach wird bis inklusive dem letzten Beitrag
    geladen"""
    bat_exported = pv_exported = cp_imported = counter_imported = 2000
    date = datetime.datetime.strptime(date, "%m/%d/%Y, %H:%M")
    daily_log = {"entries": []}
    for i in range(0, num_of_intervalls):
        if i != 0:
            bat_exported += 1000
            pv_exported += 500
            cp_imported += 2000
            counter_imported += 500
        daily_log["entries"].append({'bat': {'all': {'exported': bat_exported, 'imported': 2000, 'soc': 100},
                                             'bat2': {'exported': bat_exported, 'imported': 2000, 'soc': 100}},
                                     'counter': {'counter0': {'exported': 2000,
                                                              'grid': True,
                                                              'imported': counter_imported}},
                                     'cp': {'all': {'exported': 0, 'imported': cp_imported},
                                            'cp4': {'exported': 0, 'imported': cp_imported}},
                                     'date': date.strftime("%H:%M"),
                                     'ev': {'ev0': {'soc': None}},
                                     'hc': {'all': {'imported': 0}},
                                     'pv': {'all': {'exported': pv_exported}, 'pv1': {'exported': pv_exported}},
                                     'sh': {},
                                     'timestamp': date.timestamp()})
        date += datetime.timedelta(minutes=5)
    mock_todays_daily_log = Mock(return_value=daily_log)
    monkeypatch.setattr(chargelog, "get_todays_daily_log", mock_todays_daily_log)
    return daily_log


@pytest.fixture()
def mock_data() -> None:
    data.data_init(Mock())
    data.data.optional_data.et_module = None


def mock_create_entry_reference_end(clock, daily_log, monkeypatch):
    current_log = daily_log["entries"][-1]
    current_log["cp"]["all"]["imported"] += 500
    current_log["cp"]["cp4"]["imported"] += 500
    current_log["counter"]["counter0"]["imported"] += 500
    current_log["date"] = clock
    current_log["timestamp"] = datetime.datetime.strptime(f"05/16/2022, {clock}", "%m/%d/%Y, %H:%M").timestamp()
    mock_create_entry = Mock(return_value=current_log)
    monkeypatch.setattr(chargelog, "create_entry", mock_create_entry)


def init_cp(charged_energy, charged_energy_by_source, start_hour, start_minute=47):
    cp = Chargepoint(4, None)
    cp.data.set.log.imported_since_plugged = cp.data.set.log.imported_since_mode_switch = charged_energy
    cp.data.set.log.timestamp_start_charging = datetime.datetime(2022, 5, 16, start_hour, start_minute).timestamp()
    cp.data.get.imported = charged_energy + 2000
    cp.data.set.log.charged_energy_by_source = charged_energy_by_source
    return cp


def test_calc_charge_cost_no_hour_change_reference_end(mock_data, monkeypatch):
    cp = init_cp(6500, empty_enery_source_dict_factory(), 8, start_minute=24)
    daily_log = mock_daily_log_with_charging("05/16/2022, 8:25", 4, monkeypatch)
    datetime_mock = MagicMock(wraps=datetime.datetime)
    datetime_mock.now.return_value = datetime.datetime.fromtimestamp(1652683252)
    monkeypatch.setattr(datetime, "datetime", datetime_mock)

    with patch("builtins.open", mock_open(read_data=json.dumps(daily_log))):
        calculate_charged_energy_by_source(cp, True)

    assert cp.data.set.log.charged_energy_by_source == {
        'grid': 1625, 'pv': 1625, 'bat': 3250, 'cp': 0.0}


def test_calc_charge_cost_no_hour_change_reference_end_no_charge_at_end(mock_data, monkeypatch):
    cp = init_cp(6500, empty_enery_source_dict_factory(), 8, start_minute=24)
    daily_log = mock_daily_log_with_charging("05/16/2022, 8:25", 4, monkeypatch)
    # großer Spung im Netzbezug, aber keine Ladung mehr, gleiches Ergebnis wie oben
    daily_log["entries"].append({'bat': {'all': {'exported': 5000, 'imported': 2000, 'soc': 100},
                                         'bat2': {'exported': 5000, 'imported': 2000, 'soc': 100}},
                                 'counter': {'counter0': {'exported': 2000,
                                                          'grid': True,
                                                          'imported': 7000}},
                                 'cp': {'all': {'exported': 0, 'imported': 8000},
                                        'cp4': {'exported': 0, 'imported': 8000}},
                                 'date': '08:45',
                                 'ev': {'ev0': {'soc': None}},
                                 'hc': {'all': {'imported': 0}},
                                 'pv': {'all': {'exported': 3500}, 'pv1': {'exported': 3500}},
                                 'sh': {},
                                 'timestamp': 1652683500})
    datetime_mock = MagicMock(wraps=datetime.datetime)
    datetime_mock.now.return_value = datetime.datetime.fromtimestamp(1652683552)
    monkeypatch.setattr(datetime, "datetime", datetime_mock)

    with patch("builtins.open", mock_open(read_data=json.dumps(daily_log))):
        calculate_charged_energy_by_source(cp, True)

    assert cp.data.set.log.charged_energy_by_source == {
        'grid': 1625, 'pv': 1625, 'bat': 3250, 'cp': 0.0}


def test_calc_charge_cost_first_hour_change_reference_begin(mock_data, monkeypatch):
    cp = init_cp(6000, empty_enery_source_dict_factory(), 7)
    daily_log = mock_daily_log_with_charging("05/16/2022, 7:45", 4, monkeypatch)
    datetime_mock = MagicMock(wraps=datetime.datetime)
    datetime_mock.now.return_value = datetime.datetime.fromtimestamp(1652680800)
    monkeypatch.setattr(datetime, "datetime", datetime_mock)

    with patch("builtins.open", mock_open(read_data=json.dumps(daily_log))):
        calculate_charged_energy_by_source(cp, False)

    assert cp.data.set.log.charged_energy_by_source == {'grid': 1500, 'pv': 1500, 'bat': 3000, 'cp': 0.0}


def test_calc_charge_cost_first_hour_change_reference_begin_day_change(mock_data, monkeypatch):
    cp = init_cp(6000, empty_enery_source_dict_factory(), 23)
    daily_log = mock_daily_log_with_charging("05/16/2022, 23:45", 4, monkeypatch)
    datetime_mock = MagicMock(wraps=datetime.datetime)
    datetime_mock.now.return_value = datetime.datetime.fromtimestamp(1652738400)
    monkeypatch.setattr(datetime, "datetime", datetime_mock)

    with patch("builtins.open", mock_open(read_data=json.dumps(daily_log))):
        calculate_charged_energy_by_source(cp, False)

    assert cp.data.set.log.charged_energy_by_source == {'grid': 1500, 'pv': 1500, 'bat': 3000, 'cp': 0.0}


def test_calc_charge_cost_one_hour_change_reference_end(mock_data, monkeypatch):
    cp = init_cp(22500, {'bat': 1000, 'cp': 0.0, 'grid': 1000, 'pv': 1000}, 7)
    daily_log = mock_daily_log_with_charging("05/16/2022, 07:45", 12, monkeypatch)
    datetime_mock = MagicMock(wraps=datetime.datetime)
    datetime_mock.now.return_value = datetime.datetime.fromtimestamp(1652683201)
    monkeypatch.setattr(datetime, "datetime", datetime_mock)

    with patch("builtins.open", mock_open(read_data=json.dumps(daily_log))):
        calculate_charged_energy_by_source(cp, True)

    assert cp.data.set.log.charged_energy_by_source == {'bat': 9250.0, 'cp': 0.0, 'grid': 5125.0, 'pv': 5125.0}


def test_calc_charge_cost_two_hour_change_reference_middle(mock_data, monkeypatch):
    cp = init_cp(22500, {'bat': 1000, 'cp': 0.0, 'grid': 1000, 'pv': 1000}, 6)
    daily_log = mock_daily_log_with_charging("05/16/2022, 06:45", 16, monkeypatch)
    mock_today_timestamp = Mock(return_value=1652680801)
    monkeypatch.setattr(timecheck, "create_timestamp", mock_today_timestamp)

    datetime_mock = MagicMock(wraps=datetime.datetime)
    datetime_mock.now.return_value = datetime.datetime.fromtimestamp(1652680801)
    monkeypatch.setattr(datetime, "datetime", datetime_mock)

    with patch("builtins.open", mock_open(read_data=json.dumps(daily_log))):
        calculate_charged_energy_by_source(cp, False)

    assert cp.data.set.log.charged_energy_by_source == {'bat': 13000.0, 'cp': 0.0, 'grid': 7000.0, 'pv': 7000.0}


def test_calc_charge_cost_two_hour_change_reference_end(mock_data, monkeypatch):
    cp = init_cp(46500, {'bat': 1000, 'cp': 0.0, 'grid': 1000, 'pv': 1000}, 6)
    daily_log = mock_daily_log_with_charging("05/16/2022, 06:45", 24, monkeypatch)

    datetime_mock = MagicMock(wraps=datetime.datetime)
    datetime_mock.now.return_value = datetime.datetime.fromtimestamp(1652683201)
    monkeypatch.setattr(datetime, "datetime", datetime_mock)

    with patch("builtins.open", mock_open(read_data=json.dumps(daily_log))):
        calculate_charged_energy_by_source(cp, True)

    assert cp.data.set.log.charged_energy_by_source == {'bat': 9250.0, 'cp': 0.0, 'grid': 5125.0, 'pv': 5125.0}
