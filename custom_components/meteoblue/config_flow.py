"""Config flow for Meteoblue integration."""

from __future__ import annotations

import asyncio
import logging
from typing import Any

import aiohttp
import voluptuous as vol
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import CONF_LATITUDE, CONF_LONGITUDE, CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import (
    API_URL_BASE,
    CONF_API_KEY,
    CONF_ELEVATION,
    DEFAULT_NAME,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_API_KEY): cv.string,
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
        vol.Optional(CONF_LATITUDE): cv.latitude,
        vol.Optional(CONF_LONGITUDE): cv.longitude,
        vol.Optional(CONF_ELEVATION): cv.positive_int,
    }
)


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect."""
    session = async_get_clientsession(hass)

    # Use provided coordinates or fall back to Home Assistant defaults
    latitude = data.get(CONF_LATITUDE, hass.config.latitude)
    longitude = data.get(CONF_LONGITUDE, hass.config.longitude)

    if latitude is None or longitude is None:
        raise ValueError("Latitude and longitude must be provided")

    # Test API call
    url = f"{API_URL_BASE}/basic-1h"
    params = {
        "lat": latitude,
        "lon": longitude,
        "apikey": data[CONF_API_KEY],
        "forecast_days": 1,
        "format": "json",
    }

    if CONF_ELEVATION in data:
        params["asl"] = data[CONF_ELEVATION]

    try:
        async with asyncio.timeout(30):
            async with session.get(url, params=params) as response:
                if response.status == 401:
                    raise InvalidAuth("Invalid API key")
                elif response.status == 429:
                    raise CannotConnect("API rate limit exceeded")
                elif response.status != 200:
                    raise CannotConnect(f"API returned status {response.status}")

                result = await response.json()

                # Return location name if available
                location_name = DEFAULT_NAME
                if "metadata" in result and "name" in result["metadata"]:
                    location_name = result["metadata"]["name"]

                return {"title": location_name}

    except asyncio.TimeoutError as ex:
        raise CannotConnect("Timeout connecting to Meteoblue API") from ex
    except aiohttp.ClientError as ex:
        raise CannotConnect(f"Error connecting to Meteoblue API: {ex}") from ex


class MeteoblueConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Meteoblue."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except ValueError:
                errors["base"] = "invalid_location"
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                # Check if already configured
                await self.async_set_unique_id(
                    f"{user_input[CONF_API_KEY]}-{user_input.get(CONF_LATITUDE, self.hass.config.latitude)}-{user_input.get(CONF_LONGITUDE, self.hass.config.longitude)}"
                )
                self._abort_if_unique_id_configured()

                return self.async_create_entry(title=info["title"], data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )


class CannotConnect(Exception):
    """Error to indicate we cannot connect."""


class InvalidAuth(Exception):
    """Error to indicate there is invalid auth."""
