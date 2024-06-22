"""Init for integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from . import const as irri
from .coordinator import IRRICoordinator


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry):
    """Setup up a config entry."""
    config = config_entry.data
    coordinator = IRRICoordinator(hass, config)

    hass.data[irri.DOMAIN] = {
        "coord": coordinator,
    }

    hass.async_create_task(
        hass.config_entries.async_forward_entry_setups(
            config_entry,
            ["sensor"],
        ),
    )

    return True
