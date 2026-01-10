"""Constants for Meteoblue component."""

from homeassistant.components.weather import (
    ATTR_CONDITION_CLEAR_NIGHT,
    ATTR_CONDITION_CLOUDY,
    ATTR_CONDITION_FOG,
    ATTR_CONDITION_LIGHTNING_RAINY,
    ATTR_CONDITION_PARTLYCLOUDY,
    ATTR_CONDITION_POURING,
    ATTR_CONDITION_RAINY,
    ATTR_CONDITION_SNOWY,
    ATTR_CONDITION_SNOWY_RAINY,
    ATTR_CONDITION_SUNNY,
    ATTR_FORECAST_CLOUD_COVERAGE,
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
    ATTR_WEATHER_CLOUD_COVERAGE,
    ATTR_WEATHER_DEW_POINT,
    ATTR_WEATHER_HUMIDITY,
    ATTR_WEATHER_PRESSURE,
    ATTR_WEATHER_TEMPERATURE,
    ATTR_WEATHER_UV_INDEX,
    ATTR_WEATHER_VISIBILITY,
    ATTR_WEATHER_WIND_BEARING,
    ATTR_WEATHER_WIND_GUST_SPEED,
    ATTR_WEATHER_WIND_SPEED,
    DOMAIN as WEATHER_DOMAIN,
)

DOMAIN = "meteoblue"

DEFAULT_NAME = "Meteoblue"
DEFAULT_SCAN_INTERVAL = 600  # 10 minutes

# Configuration keys
CONF_API_KEY = "api_key"
CONF_LATITUDE = "latitude"
CONF_LONGITUDE = "longitude"
CONF_ELEVATION = "elevation"

# API constants
API_URL_BASE = "https://my.meteoblue.com/packages"
DEFAULT_PACKAGES = "basic-1h_basic-day"
DEFAULT_FORECAST_DAYS = 7

# Meteoblue pictocodes to Home Assistant conditions mapping
# Based on Meteoblue pictocode documentation
CONDITIONS_MAP = {
    ATTR_CONDITION_SUNNY: {1, 2},  # Clear sky, Few clouds
    ATTR_CONDITION_PARTLYCLOUDY: {3, 4},  # Partly cloudy, Broken clouds
    ATTR_CONDITION_CLOUDY: {5},  # Overcast
    ATTR_CONDITION_FOG: {6, 7},  # Fog, Light fog
    ATTR_CONDITION_RAINY: {
        8,
        9,
        10,
        23,
        24,
        25,
    },  # Light rain, Rain, Heavy rain, Light shower, Shower, Heavy shower
    ATTR_CONDITION_POURING: {11, 26},  # Violent rain, Violent shower
    ATTR_CONDITION_SNOWY: {
        12,
        13,
        14,
        27,
        28,
        29,
    },  # Light snow, Snow, Heavy snow, Light snow shower, Snow shower, Heavy snow shower
    ATTR_CONDITION_SNOWY_RAINY: {
        15,
        16,
        17,
        30,
        31,
        32,
    },  # Light sleet, Sleet, Heavy sleet, Light sleet shower, Sleet shower, Heavy sleet shower
    ATTR_CONDITION_LIGHTNING_RAINY: {
        18,
        19,
        20,
        21,
        22,
        33,
        34,
        35,
    },  # Thunderstorm, Light thunderstorm, Heavy thunderstorm, Hail, Heavy hail, Light thunderstorm with rain, Thunderstorm with rain, Heavy thunderstorm with rain
    ATTR_CONDITION_CLEAR_NIGHT: {1, 2},  # Clear sky, Few clouds (night)
}

# Reverse mapping for lookup
PICTOCODE_TO_CONDITION = {}
for condition, codes in CONDITIONS_MAP.items():
    for code in codes:
        PICTOCODE_TO_CONDITION[code] = condition

# Forecast mapping
FORECAST_MAP = {
    ATTR_FORECAST_CONDITION: "condition",
    ATTR_FORECAST_NATIVE_PRECIPITATION: "precipitation",
    ATTR_FORECAST_PRECIPITATION_PROBABILITY: "precipitation_probability",
    ATTR_FORECAST_NATIVE_TEMP: "temperature_max",
    ATTR_FORECAST_NATIVE_TEMP_LOW: "temperature_min",
    ATTR_FORECAST_TIME: "time",
    ATTR_FORECAST_WIND_BEARING: "wind_direction",
    ATTR_FORECAST_NATIVE_WIND_SPEED: "wind_speed",
    ATTR_FORECAST_NATIVE_WIND_GUST_SPEED: "wind_gust",
    ATTR_FORECAST_CLOUD_COVERAGE: "cloudiness",
    ATTR_FORECAST_HUMIDITY: "relative_humidity",
    ATTR_FORECAST_UV_INDEX: "uv_index",
}

# Current weather mapping
ATTR_MAP = {
    ATTR_WEATHER_HUMIDITY: "relative_humidity",
    ATTR_WEATHER_PRESSURE: "pressure_msl",
    ATTR_WEATHER_TEMPERATURE: "temperature",
    ATTR_WEATHER_VISIBILITY: "visibility",
    ATTR_WEATHER_WIND_BEARING: "wind_direction",
    ATTR_WEATHER_WIND_SPEED: "wind_speed",
    ATTR_WEATHER_WIND_GUST_SPEED: "wind_gust",
    ATTR_WEATHER_CLOUD_COVERAGE: "cloudiness",
    ATTR_WEATHER_DEW_POINT: "dew_point",
    ATTR_WEATHER_UV_INDEX: "uv_index",
}
