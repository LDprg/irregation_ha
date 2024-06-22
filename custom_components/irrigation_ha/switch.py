"""Platform for sensor integration."""

from __future__ import annotations

from homeassistant.components.switch import SwitchEntity, SwitchDeviceClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.const import (
    STATE_UNAVAILABLE,
    STATE_UNKNOWN,
)

from . import const as irri
from .coordinator import IRRICoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    _config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Setup sensors from a config entry created in the integrations UI."""
    coordinator: IRRICoordinator = hass.data[irri.DOMAIN]["coord"]

    async_add_entities(
        [IRRISwitch(coordinator, name) for name in ["active"]],
    )


class IRRISwitch(CoordinatorEntity, SwitchEntity, RestoreEntity):
    """Representation of a Sensor."""

    def __init__(self, coordinator, uid):
        """Pass coordinator to CoordinatorEntity."""
        super().__init__(coordinator)

        self._attr_name = uid
        self._attr_unique_id = uid

        self._attr_device_class = SwitchDeviceClass.SWITCH

    async def async_added_to_hass(self) -> None:
        """Restore last state."""
        await super().async_added_to_hass()
        if (last_state := await self.async_get_last_state()) is not None:
            if last_state.state not in (STATE_UNKNOWN, STATE_UNAVAILABLE):
                self._attr_is_on = bool(last_state.state)
            elif last_state.state is STATE_UNKNOWN:
                self._attr_is_on = True

    async def async_turn_on(self, **kwargs):
        """Turn the entity on."""
        self._attr_is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        """Turn the entity off."""
        self._attr_is_on = False
        self.async_write_ha_state()
