import requests
import os
import re
from datetime import datetime
import pytz

def fetch_weather():
    # Fetching weather for New York as a default/example location
    # Lat/Lon for New York: 40.7128, -74.0060
    url = "https://api.open-meteo.com/v1/forecast?latitude=40.7128&longitude=-74.0060&current_weather=true"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data['current_weather']
    except Exception as e:
        print(f"Error fetching weather: {e}")
        return None

def get_weather_description(code):
    # WMO Weather interpretation codes (WW)
    weather_codes = {
        0: 'Clear sky',
        1: 'Mainly clear', 2: 'Partly cloudy', 3: 'Overcast',
        45: 'Fog', 48: 'Depositing rime fog',
        51: 'Light drizzle', 53: 'Moderate drizzle', 55: 'Dense drizzle',
        61: 'Slight rain', 63: 'Moderate rain', 65: 'Heavy rain',
        71: 'Slight snow fall', 73: 'Moderate snow fall', 75: 'Heavy snow fall',
        95: 'Thunderstorm', 96: 'Thunderstorm with slight hail', 99: 'Thunderstorm with heavy hail'
    }
    return weather_codes.get(code, 'Unknown weather status')

def update_readme(weather_data):
    if not weather_data:
        return

    temperature = weather_data['temperature']
    windspeed = weather_data['windspeed']
    weathercode = weather_data['weathercode']
    description = get_weather_description(weathercode)
    
    # Get current time in EST
    est = pytz.timezone('US/Eastern')
    now = datetime.now(est).strftime('%Y-%m-%d %H:%M:%S %Z')

    weather_text = (
        f"**Current Weather in New York:**\n"
        f"- 🌡️ **Temperature:** {temperature}°C\n"
        f"- 🌬️ **Wind Speed:** {windspeed} km/h\n"
        f"- 🌤️ **Condition:** {description}\n"
        f"- 🕒 **Last Updated:** {now}"
    )

    readme_path = 'README.md'
    
    with open(readme_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Regex to replace content between markers
    pattern = r'(<!-- WEATHER_START -->)(.*?)(<!-- WEATHER_END -->)'
    replacement = f'\\1\n{weather_text}\n\\3'
    
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    with open(readme_path, 'w', encoding='utf-8') as file:
        file.write(new_content)

if __name__ == "__main__":
    data = fetch_weather()
    update_readme(data)
