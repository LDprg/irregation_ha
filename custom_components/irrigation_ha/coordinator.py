' Coordinator file '
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from . import const as irri


class IRRICoordinator(DataUpdateCoordinator):
    """Irrigation coordinator."""

    def __init__(self, hass, config):
        """Initialize the coordinator"""
        super().__init__(
            hass,
            irri.LOGGER,
            name=irri.DOMAIN,
        )
        self.hass = hass
        self.config = config
