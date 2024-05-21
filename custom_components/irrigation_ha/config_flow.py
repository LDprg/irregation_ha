"""Config flow for integration."""
from __future__ import annotations

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.components.binary_sensor import (
    DOMAIN as BINARY_SENSOR_DOMAIN,
)
from homeassistant.components.switch import DOMAIN as SWITCH_DOMAIN
from homeassistant.config_entries import ConfigFlow
from homeassistant.const import CONF_COUNT
from homeassistant.const import CONF_ENTITY_ID

from . import const as irri


class IrrigationHaFlow(ConfigFlow, domain=irri.DOMAIN):
    """
    Irrigation HA config flow
    """

    async def async_step_user(
            self, _user_input,
    ):
        """
        Init step
        """

        return self.async_show_form(
            step_id='user',
            data_schema=vol.Schema({
                vol.Required(CONF_COUNT, default=1): cv.positive_int,
                vol.Required(CONF_ENTITY_ID): vol.Any(
                    cv.entity_domain(BINARY_SENSOR_DOMAIN),
                    cv.entity_domain(SWITCH_DOMAIN),
                ),
            }),
        )
