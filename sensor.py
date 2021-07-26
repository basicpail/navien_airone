import logging
from datetime import timedelta
from ast import literal_eval

from navien_airone.navien_airone import NavienAirone

from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers import device_registry as dr
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.typing import HomeAssistantType
from homeassistant.const import ATTR_NAME, CONF_USERNAME, CONF_PASSWORD, CONF_DEVICES

from homeassistant.const import (
    TEMP_CELSIUS,
    PERCENTAGE,
)

from .const import DOMAIN,CONF_DEVICEID,NAVIEN_SENSOR,NAVIEN_SWITCH

ATTRIBUTION = ("This is remote controller for KyoungDong Navien Airone")

DEFAULT_NAME = "Navien Aireone"

_LOGGER = logging.getLogger(__name__)

#SCAN_INTERVAL = timedelta(seconds=30)

STATUS_CATEGORY = [
    "desiredTemperature",
    "currentTemperature",
	"desiredHumidity",
	"currentHumidity",
    "isRunning",
    "current_operationmode",
]

async def async_setup_entry(hass, config_entry, async_add_entities):
    #print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@navien hass.data[DOMAIN]hass.data[DOMAIN]: ")
    #print(hass.data[DOMAIN])
    #print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@navien hass.data[DOMAIN]hass.data[DOMAIN][config_entry.entry_id]:")
    #print(hass.data[DOMAIN][config_entry.entry_id])
    coordinator = hass.data[DOMAIN][NAVIEN_SENSOR]
    #_LOGGER.info(f"navien coordinator : {coordinator}")

    entities = []
    for i,status_category in enumerate(STATUS_CATEGORY):
        entities.append(NavienBaseSensor(coordinator, config_entry.data, status_category))

    async_add_entities(entities)
    
    #entities.append(NavienBaseSensor(coordinator,config_entry.data))

class NavienBaseSensor(CoordinatorEntity,Entity):

    def __init__(self, coordinator, config, STATUS_CATEGORY):
        """Initialise the platform with a data instance and site."""
        super().__init__(coordinator)
        self._config = config
        self._data_type = STATUS_CATEGORY
        #self._current_operationmode = NavienAirone(deviceid=self._config.get(CONF_DEVICEID))

    @property
    def unique_id(self):
        """Return unique ID."""
        _LOGGER.info(f"navien def unique_id {self._config[CONF_DEVICEID]}{self._data_type}")
        return f"{self._config[CONF_DEVICEID]} {self._data_type}"

    @property
    def name(self):
        """Return the name of the sensor."""
        name = self._config.get(CONF_DEVICEID)
        _LOGGER.info(f"navien def name {DEFAULT_NAME} {self._data_type}")
        return f"{DEFAULT_NAME} {self._data_type}"

    @property
    def state(self):
        # _LOGGER.info(f"navienmsg18 state dir(self.coordinator) : {dir(self.coordinator.data.hass.states)}")
        # _LOGGER.info(f"navienmsg18 state vars(self.coordinator.data) : {vars(self.coordinator.data.hass.states)}")
        # _LOGGER.info(f"navienmsg18 state self.coordinator.data : {self.coordinator.data.hass.statess}")

        # _LOGGER.info(f"navienmsg18 state dir self.coordinator.statusvalue : {dir(self.coordinator.statusvalue)}")
        # _LOGGER.info(f"navienmsg18 state vars self.coordinator.statusvalue : {vars(self.coordinator.statusvalue)}")
        # _LOGGER.info(f"navienmsg18 state self.coordinator.statusvalue : {self.coordinator.statusvalue}")

        if self.coordinator.data.current_status_data == None:
            return "uploading.."

        if self._data_type == "desiredTemperature":
            _LOGGER.info(f"navien self.coordinator.data.current_status_data: {self.coordinator.data.current_status_data}")
            temp_dict1 = self.coordinator.data.current_status_data.decode()
            tmep_dict2 = literal_eval(temp_dict1)
            return tmep_dict2["request"]["desiredTemperature"]

        if self._data_type == "currentTemperature":
            temp_dict1 = self.coordinator.data.current_status_data.decode()
            tmep_dict2 = literal_eval(temp_dict1)
            return tmep_dict2["request"]["currentTemperature"]

        if self._data_type == "desiredHumidity":
            temp_dict1 = self.coordinator.data.current_status_data.decode()
            tmep_dict2 = literal_eval(temp_dict1)
            return tmep_dict2["request"]["currentHumidity"]

        if self._data_type == "currentHumidity":
            temp_dict1 = self.coordinator.data.current_status_data.decode()
            tmep_dict2 = literal_eval(temp_dict1)
            return tmep_dict2["request"]["currentHumidity"]

        if self._data_type == "isRunning":
            temp_dict1 = self.coordinator.data.current_status_data.decode()
            tmep_dict2 = literal_eval(temp_dict1)
            if tmep_dict2["request"]["isRunning"] == 1:
                return "off"
            else:
                return "on"
        
        if self._data_type == "current_operationmode":
            return self.coordinator.data.hass.states.get('sensor.navien_aireone_current_operationmode').state


    @property
    def unit_of_measurement(self):
        if self._data_type == "desiredTemperature":
            return TEMP_CELSIUS

        elif self._data_type == "currentTemperature":
            return TEMP_CELSIUS
        
        elif self._data_type == "desiredHumidity":
            return PERCENTAGE

        elif self._data_type == "currentHumidity":
            return PERCENTAGE


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