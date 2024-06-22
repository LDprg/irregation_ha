"""Platform for sensor integration."""

from __future__ import annotations
from datetime import time

from homeassistant.components.time import TimeEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

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
        [IRRITime(coordinator, name) for name in ["start_time"]],
    )


class IRRITime(CoordinatorEntity, TimeEntity):
    """Representation of a Sensor."""

    def __init__(self, coordinator, uid):
        """Pass coordinator to CoordinatorEntity."""
        super().__init__(coordinator)

        self._attr_name = uid
        self._attr_unique_id = uid

    async def async_added_to_hass(self) -> None:
        """When entity is added to Home Assistant."""
        await super().async_added_to_hass()
        last_number_data = await self.async_get_last_number_data()
        if (last_number_data is not None) and (
            last_number_data.native_value is not None
        ):
            await self.async_set_native_value(last_number_data.native_value)

    async def async_set_value(self, value: time) -> None:
        """Update the current value."""
        self._attr_native_value = value
        self.async_write_ha_state()
