"""The navien component."""
from __future__ import annotations
from datetime import timedelta
import logging
from random import randrange

from navien_airone.navien_airone import NavienAirone
#from navien.navien_airone import protocol

from homeassistant.core import Config, HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.helpers.restore_state import RestoreEntity



from .const import DOMAIN,CONF_DEVICEID,SUPPORT_TYPE,NAVIEN_SENSOR,NAVIEN_SWITCH
DATA_INSTANCE = "recorder_instance"
_LOGGER = logging.getLogger(__name__)


request = {
                "clientId": "98D8630F60FA146E",
                "sessionId": "",
                "requestTopic":"cmd/rc/2/98D8630F60FA146E/remote/status",
                "responseTopic": "cmd/rc/2/98D8630F60FA146E/remote/status/res"
                }

# def async_setup_platform(hass:HomeAssistant, config, async_add_devices, discovery_info=None):
#     entities = []
#     entities.append(input_number.InputNumber(navien_inputnumber, config_entry.data, "inputnumber_test"))
#     async_add_devices(entities)

async def async_setup(hass: HomeAssistant, config: Config) -> bool:
    """Set up configured navien"""
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass, config_entry):
    """Set up PubAir as config entry."""
    coordinator = NavienDataUpdateCoordinator(hass, config_entry)
    navien_controller = NavienSwitch(hass, config_entry)
    custom_config = []
    custom_config.append(coordinator)
    custom_config.append(navien_controller)

    await coordinator.async_refresh()

    if not coordinator.last_update_success:
        raise ConfigEntryNotReady
    #hass.data[DOMAIN][config_entry.entry_id].add(custom_config)
    #hass.data[DOMAIN][config_entry.entry_id] = coordinator
    hass.data[DOMAIN][NAVIEN_SENSOR] = coordinator
    hass.data[DOMAIN][NAVIEN_SWITCH] = navien_controller


    #config_entry.data[CUSTOM_CONFIG]

    #print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@navien hass.data[DOMAIN]hass.data[DOMAIN]: ")
    #print(hass.data[DOMAIN])
    #print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@navien hass.data[DOMAIN]hass.data[DOMAIN][config_entry.entry_id]:")
    #print(hass.data[DOMAIN][config_entry])

    for domain in SUPPORT_TYPE:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(config_entry, domain) #whats config_entry exactly
        )

    return True

async def async_unload_entry(hass, config_entry):
    """Unload a config entry."""
    for domain in SUPPORT_TYPE:
        await hass.config_entries.async_forward_entry_unload(config_entry, domain)
        hass.data[DOMAIN].pop(config_entry.entry_id)

    return True


class NavienDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Navien data."""

    def __init__(self, hass, config_entry):
        """Initialize global Navien data updater."""
        self._unsub_track_home = None
        self.statusvalue = NavienStatusData(hass, config_entry.data)
        self.statusvalue.init_data()

        update_interval = timedelta(seconds=randrange(60, 70))
        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=update_interval)

    async def _async_update_data(self):
        """Fetch data from Navien"""
        _LOGGER.info("function _async_update_data was called")
        print("_async_update_data was called")
        try:
            return await self.statusvalue.fetch_data()
        except Exception as err:
            raise UpdateFailed(f"Update failed: {err}") from err


class NavienStatusData:
    def __init__(self, hass, config):
        """Initialise the Navien entity data."""
        self.hass = hass
        self._config = config
        self.current_status_data = {}
        self.current_client_data = {}

    def init_data(self):
        """get the coordinates."""
        _LOGGER.info(f"navien self._config.get(CONF_DEVICEID): {self._config.get(CONF_DEVICEID)}") #CONF_DEVICE : userinput
        self._navien_data_sub = NavienAirone(deviceid=self._config.get(CONF_DEVICEID))
        self._navien_data_sub.sub_threading()
        
        
        self._navien_data_pub = NavienAirone(deviceid=self._config.get(CONF_DEVICEID))
        self._navien_data_pub.publish_once(requesttopic=self._navien_data_pub.build_topic("device_status"),body=request)
        self.current_status_data = self._navien_data_sub._payload

    async def fetch_data(self):
        """Fetch data from API"""
        #await self._navien_data.fetching_data()
        
        self._navien_data_pub.publish_once(requesttopic=self._navien_data_pub.build_topic("device_status"),body=request)
        self.current_status_data = self._navien_data_sub._payload
        _LOGGER.info(f"navien class NavienStatusData self.current_status_data: {self.current_status_data}")
        return self


class NavienSwitch(DataUpdateCoordinator):
    def __init__(self, hass, config):
        """Initialise the Navien entity data."""
        self.hass = hass
        self._config = config
        self.current_status_data = {}

        self._requesttopic = None
        self._operationmode = None
        self._optionmode = None
        self._windlevel = None
        self._hass_recorder = hass.data[DATA_INSTANCE]

    #def give_order(self,requestTopic,request)
    def give_order(
        self,requesttopic=None,
        operationmode=None,
        optionmode : "optionmode or schedule time" = None,
        windlevel : "windlevel or deepsleep time" = None
        ):
        try:
            self._navien_switch_pub = NavienAirone(deviceid=self._config.data[CONF_DEVICEID])
            #await self._navien_data.fetching_data()
            
            """
            request = {
                        "clientId": "98D8630F60FA146E",
                        "sessionId": "",
                        "requestTopic": "cmd/rc/2/98D8630F60FA146E/remote/power",
                        "responseTopic": "cmd/rc/2/98D8630F60FA146E/remote/status/res",
                        "request":{"power":command}
                    }

            request = {
                        "clientId": "98D8630F60FA146E",
                        "sessionId": "",
                        "requestTopic": "cmd/rc/2/98D8630F60FA146E/remote/power",
                        "responseTopic": "cmd/rc/2/98D8630F60FA146E/remote/status/res",
                        "request":{"power":command}
                    }

                    
            """

            #_LOGGER.info(f"navien self._navien_data.build_topic: {self._navien_data.build_topic()}")
            #self._navien_data.create_subscriber()
            if requesttopic is not None:
                self._requesttopic = requesttopic
            if operationmode is not None:
                self._operationmode = operationmode
            if optionmode is not None:
                self._optionmode = optionmode
            if windlevel is not None:
                self._windlevel = windlevel

            request = self._navien_switch_pub.build_payload(self._requesttopic,self._operationmode,self._optionmode,self._windlevel)
            _LOGGER.info(f"navienmsg request: {request}")
            self._navien_switch_pub.publish_once(self._navien_switch_pub.build_topic(self._requesttopic),body=request)

            return self
        except Exception as e:
            _LOGGER.info(f"naveienmsg error:{e}")
