"""The Meteoblue integration."""

from __future__ import annotations

import logging

from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .coordinator import MeteoblueConfigEntry, MeteoblueDataUpdateCoordinator

PLATFORMS = [Platform.WEATHER]

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, config_entry: MeteoblueConfigEntry
) -> bool:
    """Set up Meteoblue as config entry."""
    coordinator = MeteoblueDataUpdateCoordinator(hass, config_entry)
    await coordinator.async_config_entry_first_refresh()

    config_entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(config_entry, PLATFORMS)

    return True


async def async_unload_entry(
    hass: HomeAssistant, config_entry: MeteoblueConfigEntry
) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(config_entry, PLATFORMS)
