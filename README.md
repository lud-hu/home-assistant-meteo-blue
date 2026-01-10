# Meteoblue Home Assistant Integration

This is a custom Home Assistant integration for the Meteoblue weather service API. It provides weather data including current conditions, hourly forecasts, and daily forecasts.

## Features

- Current weather conditions
- Hourly forecasts (next 24 hours)
- Daily forecasts (up to 7 days)
- Configurable location coordinates
- API key authentication
- Automatic weather condition mapping from Meteoblue pictocodes

## Installation

### HACS (Recommended)

1. Add this repository to HACS as a custom repository
2. Install the integration through HACS
3. Restart Home Assistant

### Manual Installation

1. Copy the `meteoblue` folder to your `custom_components` directory
2. Restart Home Assistant

## Configuration

### Prerequisites

You need a Meteoblue API key to use this integration. You can obtain one from:
https://content.meteoblue.com/en/business-solutions/weather-apis

### Setup

1. Go to **Settings** → **Devices & Services**
2. Click **Add Integration**
3. Search for "Meteoblue"
4. Enter your configuration:
   - **API Key**: Your Meteoblue API key (required)
   - **Name**: A name for this weather station (optional, defaults to "Meteoblue")
   - **Latitude**: Location latitude (optional, uses Home Assistant location if not provided)
   - **Longitude**: Location longitude (optional, uses Home Assistant location if not provided)
   - **Elevation**: Location elevation in meters (optional, auto-detected if not provided)

## API Usage

The integration uses the Meteoblue Forecast API with the following packages:

- `basic-1h`: Hourly temperature, humidity, wind, precipitation
- `basic-day`: Daily min/max temperatures and weather conditions

The API is called every 10 minutes by default to fetch updated weather data.

## Supported Weather Attributes

### Current Weather

- Temperature
- Humidity
- Pressure
- Wind speed and direction
- Wind gust speed
- Visibility
- UV index
- Weather condition

### Forecasts

- Temperature (min/max for daily)
- Precipitation amount and probability
- Wind speed, direction, and gusts
- Humidity
- Weather condition
- UV index

## Weather Condition Mapping

Meteoblue pictocodes are automatically mapped to Home Assistant weather conditions:

- Clear/Sunny
- Partly Cloudy
- Cloudy
- Fog
- Rainy
- Snowy
- Snow/Rain mix
- Thunderstorm

## Troubleshooting

### Common Issues

1. **Invalid API Key**: Verify your Meteoblue API key is correct and has sufficient quota
2. **Cannot Connect**: Check your internet connection and API endpoint availability
3. **Rate Limit Exceeded**: Reduce polling frequency or check your API usage limits

### Logging

To enable debug logging for this integration, add the following to your `configuration.yaml`:

```yaml
logger:
  logs:
    custom_components.meteoblue: debug
```

## API Limits

Be aware of your Meteoblue API limits:

- Free tier typically allows 1000 calls per day
- Rate limit of 500 calls per minute
- Monitor your usage in the Meteoblue dashboard

## Contributing

This integration is based on the official Met.no integration structure and follows Home Assistant development guidelines.

## License

This project is provided as-is for educational and personal use.
