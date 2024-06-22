"""Platform for sensor integration."""

from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback
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
        [IRRISensor(coordinator, name) for name in ["state"]],
    )


class IRRISensor(CoordinatorEntity, SensorEntity):
    """Representation of a Sensor."""

    def __init__(self, coordinator, uid):
        """Pass coordinator to CoordinatorEntity."""
        super().__init__(coordinator)

        self._attr_name = uid
        self._attr_unique_id = uid

        self._attr_native_value = self.coordinator.hass.states.get(
            "input_boolean.test",
        ).state

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        irri.LOGGER.warn(f"RECEIVED DATA: {self.coordinator.data}")

        self._attr_native_value = self.coordinator.data["input_boolean.test"]
        self.async_write_ha_state()
