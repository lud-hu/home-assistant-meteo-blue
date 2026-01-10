"""Weather entity for Meteoblue."""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

from homeassistant.components.weather import (
    ATTR_FORECAST_CONDITION,
    ATTR_FORECAST_HUMIDITY,
    ATTR_FORECAST_NATIVE_PRECIPITATION,
    ATTR_FORECAST_NATIVE_TEMP,
    ATTR_FORECAST_NATIVE_TEMP_LOW,
    ATTR_FORECAST_NATIVE_WIND_GUST_SPEED,
    ATTR_FORECAST_NATIVE_WIND_SPEED,
    ATTR_FORECAST_PRECIPITATION_PROBABILITY,
    ATTR_FORECAST_TIME,
    ATTR_FORECAST_UV_INDEX,
    ATTR_FORECAST_WIND_BEARING,
    Forecast,
    WeatherEntity,
    WeatherEntityFeature,
)
from homeassistant.const import (
    CONF_NAME,
    UnitOfLength,
    UnitOfPrecipitationDepth,
    UnitOfPressure,
    UnitOfSpeed,
    UnitOfTemperature,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util import dt as dt_util

from .const import ATTR_MAP, DEFAULT_NAME, DOMAIN, ENABLE_DEBUG_LOGGING
from .coordinator import MeteoblueConfigEntry, MeteoblueDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

# Disable debug logging if flag is False
if not ENABLE_DEBUG_LOGGING:
    _LOGGER.setLevel(logging.INFO)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: MeteoblueConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Meteoblue weather entity."""
    _LOGGER.debug("Setting up Meteoblue weather entity")
    coordinator = config_entry.runtime_data
    name = config_entry.data.get(CONF_NAME, DEFAULT_NAME)

    _LOGGER.info("Creating weather entity: %s", name)
    weather_entity = MeteoblueWeatherEntity(coordinator, name)
    async_add_entities([weather_entity], False)
    _LOGGER.debug("Weather entity added successfully")


class MeteoblueWeatherEntity(WeatherEntity):
    """Implementation of Meteoblue weather entity."""

    _attr_has_entity_name = True
    _attr_name = None
    _attr_native_temperature_unit = UnitOfTemperature.CELSIUS
    _attr_native_precipitation_unit = UnitOfPrecipitationDepth.MILLIMETERS
    _attr_native_pressure_unit = UnitOfPressure.HPA
    _attr_native_wind_speed_unit = UnitOfSpeed.METERS_PER_SECOND
    _attr_native_visibility_unit = UnitOfLength.KILOMETERS
    _attr_supported_features = WeatherEntityFeature.FORECAST_DAILY

    def __init__(
        self,
        coordinator: MeteoblueDataUpdateCoordinator,
        name: str,
    ) -> None:
        """Initialize the weather entity."""
        _LOGGER.debug("Initializing weather entity: %s", name)
        self.coordinator = coordinator
        self._attr_device_info = {
            "identifiers": {(DOMAIN, coordinator.config_entry.entry_id)},
            "name": name,
            "manufacturer": "Meteoblue",
            "model": "Weather API",
            "configuration_url": "https://www.meteoblue.com/",
        }
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}_weather"
        _LOGGER.debug(
            "Weather entity initialized with unique_id: %s", self._attr_unique_id
        )

    @property
    def available(self) -> bool:
        """Return if weather data is available."""
        return (
            self.coordinator.last_update_success
            and self.coordinator.current_weather is not None
        )

    @property
    def native_temperature(self) -> float | None:
        """Return the temperature."""
        if current := self.coordinator.current_weather:
            return current.get("temperature")
        return None

    @property
    def humidity(self) -> int | None:
        """Return the humidity."""
        if current := self.coordinator.current_weather:
            humidity = current.get("relative_humidity")
            return round(humidity) if humidity is not None else None
        return None

    @property
    def native_pressure(self) -> float | None:
        """Return the pressure."""
        if current := self.coordinator.current_weather:
            return current.get("pressure_msl")
        return None

    @property
    def native_wind_speed(self) -> float | None:
        """Return the wind speed."""
        if current := self.coordinator.current_weather:
            return current.get("wind_speed")
        return None

    @property
    def wind_bearing(self) -> float | None:
        """Return the wind bearing."""
        if current := self.coordinator.current_weather:
            return current.get("wind_direction")
        return None

    @property
    def native_wind_gust_speed(self) -> float | None:
        """Return the wind gust speed."""
        if current := self.coordinator.current_weather:
            return current.get("wind_gust")
        return None

    @property
    def native_visibility(self) -> float | None:
        """Return the visibility."""
        if current := self.coordinator.current_weather:
            visibility = current.get("visibility")
            return (
                visibility / 1000 if visibility is not None else None
            )  # Convert m to km
        return None

    @property
    def condition(self) -> str | None:
        """Return the current condition."""
        if current := self.coordinator.current_weather:
            return current.get("condition")
        return None

    @property
    def uv_index(self) -> float | None:
        """Return the UV index."""
        if current := self.coordinator.current_weather:
            return current.get("uv_index")
        return None

    async def async_forecast_daily(self) -> list[Forecast] | None:
        """Return the daily forecast."""
        _LOGGER.debug("Fetching daily forecast")
        if not self.coordinator.daily_forecast:
            _LOGGER.debug("No daily forecast data available")
            return None

        forecasts = []
        _LOGGER.debug(
            "Processing %s daily forecast entries", len(self.coordinator.daily_forecast)
        )
        for i, day_data in enumerate(self.coordinator.daily_forecast):
            _LOGGER.debug("Processing daily forecast %s: %s", i, day_data.get("time"))
            forecast = Forecast(
                datetime=dt_util.parse_datetime(day_data["time"]),
                condition=day_data.get("condition"),
                native_temperature=day_data.get("temperature_max"),
                native_templow=day_data.get("temperature_min"),
                native_precipitation=day_data.get("precipitation"),
                precipitation_probability=day_data.get("precipitation_probability"),
                wind_bearing=day_data.get("wind_direction"),
                native_wind_speed=day_data.get("wind_speed"),
                native_wind_gust_speed=day_data.get("wind_gust"),
                humidity=day_data.get("relative_humidity"),
                uv_index=day_data.get("uv_index"),
            )
            forecasts.append(forecast)

        _LOGGER.debug("Generated %s daily forecasts", len(forecasts))
        return forecasts

    async def async_update(self) -> None:
        """Update the entity."""
        _LOGGER.debug("Manual update requested for weather entity")
        await self.coordinator.async_request_refresh()
        _LOGGER.debug("Manual update completed")

    async def async_added_to_hass(self) -> None:
        """When entity is added to hass."""
        _LOGGER.info("Weather entity %s added to Home Assistant", self._attr_unique_id)
        await super().async_added_to_hass()
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )
        _LOGGER.debug("Coordinator listener registered for weather entity")
