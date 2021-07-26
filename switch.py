from __future__ import annotations
import logging
from datetime import timedelta
from typing import Any
import time

from navien_airone.navien_airone import NavienAirone

from homeassistant.components.switch import DOMAIN as DEVICE_DOMAIN, SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity import Entity
from homeassistant.components.recorder import Recorder
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.helpers.event import Event, async_track_entity_registry_updated_event


from .const import DOMAIN,CONF_DEVICEID,NAVIEN_SENSOR,NAVIEN_SWITCH

ATTRIBUTION = ("This is remote controller for KyoungDong Navien Airone")

DEFAULT_NAME = "Navien Aireone"

_LOGGER = logging.getLogger(__name__)

CONTROL_CATEGORY = [
    "power",
    "General_ventilation",
    "Air_cleaning",
    "Automatic_operation",
    "Schedule",
    "Deep_sleep"
]



async def async_setup_entry(hass, config_entry, async_add_entities):
    navien_controller = hass.data[DOMAIN][NAVIEN_SWITCH]

    #_LOGGER.info(f"navien navien_controller : {navien_controller}")

    entities = []
    #entities.append(InputNumber(navien_inputnumber, config_entry.data, "inputnumber_test"))
    for i,control_category in enumerate(CONTROL_CATEGORY):
        entities.append(NavienBaseSwitch(hass.states,navien_controller, config_entry.data, control_category,Event))

    async_add_entities(entities)

class NavienBaseSwitch(SwitchEntity,Entity):
    def __init__(self, hass_states,navien_controller, config, control_category ,Event):
        """Initialise the platform with a data instance and site."""
        self._navien_controller = navien_controller
        self._config = config
        self._control_category = control_category
        self._event = Event.data
        self.cnt = 0

        self._states = hass_states

    @property
    def unique_id(self):
        """Return unique ID."""
        _LOGGER.info(f"navien def unique_id {self._config[CONF_DEVICEID]}{self._control_category}")
        return f"{self._config[CONF_DEVICEID]} {self._control_category}"

    @property
    def name(self):
        """Return the name of the sensor."""
        name = self._config.get(CONF_DEVICEID)
        _LOGGER.info(f"navien def name {DEFAULT_NAME}{self._control_category}")
        return f"{DEFAULT_NAME} {self._control_category}"

    @property
    def is_on(self) :
        """Return true if switch is on."""
        if self.cnt >=1:
            return True
       


    #event.data.get("new_state")
    def turn_on(self, **kwargs: Any):
        """Turn the switch on."""
        if self.cnt == 0:
            self.cnt +=1
           

        if self._control_category == "power":
            self._navien_controller.give_order(
                "power",
                "power_on",
                None,
                None
            )

            self._states.set(
                entity_id = 'sensor.navien_aireone_current_operationmode',
                new_state = f"stand_by",
                attributes = self._states.get('sensor.navien_aireone_current_operationmode').attributes ##
            )

        elif self._control_category == "General_ventilation":
            self._navien_controller.give_order(
                "change_mode",
                "operation_mode_generalventilation",
                self._states.get('input_select.navien_select_option_gv').state,
                self._states.get('input_select.navien_select_windlevel_gv').state
            )

            self.set_new_state(self._control_category)


        elif self._control_category == "Air_cleaning":
            self._navien_controller.give_order(
                "change_mode",
                "operation_mode_cleaning",
                self._states.get('input_select.navien_select_option_ac').state,
                self._states.get('input_select.navien_select_windlevel_ac').state
            )

            self.set_new_state(self._control_category)

        elif self._control_category == "Automatic_operation":
            self._navien_controller.give_order(
                "change_mode",
                "operation_mode_automaticoperation",
                "nothing",
                "notset"
            )

            self.set_new_state(self._control_category)
        
        elif self._control_category == "Schedule":
            self._navien_controller.give_order(
                "schedule",
                self._states.get('input_select.navien_select_schedule').state,
                self._states.get('input_text.navien_schedule_input').state,
                None
            )

        elif self._control_category == "Deep_sleep":
            self._navien_controller.give_order(
                "deep_sleep",
                "enable_deepsleep_power_on",
                self._states.get('input_text.navien_deepsleep_start_input').state,
                self._states.get('input_text.navien_deepsleep_end_input').state
            )

    
    

    def turn_off(self, **kwargs: Any):
        """Turn the device off."""
        _LOGGER.info("navien come into turn_off")
        if self._control_category == "power":
            self._navien_controller.give_order(
                "power",
                "power_off"
                )

            self._states.set(
                    entity_id = 'sensor.navien_aireone_current_operationmode',
                    new_state = "off",
                    attributes = self._states.get('sensor.navien_aireone_current_operationmode').attributes ##
                )

        elif self._control_category == "Schedule":
                self._navien_controller.give_order(
                    "schedule",
                    "enable_disable_reservation",
                    '00:00',
                    None
                )

        elif self._control_category == "Deep_sleep":
                self._navien_controller.give_order(
                    "deep_sleep",
                   "enable_deepsleep_power_off",
                    self._states.get('input_text.navien_deepsleep_start_input').state,
                    self._states.get('input_text.navien_deepsleep_end_input').state
                )
            
        if self.cnt >= 1:
            _LOGGER.info("navien come into turn_off if")
            self.cnt = 0


    def set_new_state(self,control_category):
        self._states.set(
                    entity_id = 'sensor.navien_aireone_current_operationmode',
                    new_state = f"{control_category}",
                    attributes = self._states.get('sensor.navien_aireone_current_operationmode').attributes ##
                )


    @property
    def attribution(sefl):
        return ATTRIBUTION

    @property
    def device_info(self):
        """Device info."""
        return {
            "identifiers": {(DOMAIN,)},
            "manufacturer": "Navien",
            "model": "Airone",
            "default_name": "Navien Airone",
            "entry_type": "device", ##
        }

