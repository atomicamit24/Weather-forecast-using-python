#Step 1: Set up the basic structure and imports

import requests
import json
import pyttsx3  # For text-to-speech on Windows (optional)

#Step 2: Create a function to get weather data

def get_weather(city):
    api_key = "428db8443c15458cb9955436252507"
    url = f"https://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&alerts=yes"
    try:
        response = requests.get(url, timeout=5)  # timeout to prevent hang
        response.raise_for_status()  # Raises error for bad responses (4xx, 5xx)
        data = response.json()
        # Check if 'location' and 'current' keys exist in result
        if "location" in data and "current" in data:
            return data, None
        else:
            return None, "Unexpected response format"
    except requests.exceptions.HTTPError as http_err:
        return None, f"HTTP error occurred: {http_err}"
    except requests.exceptions.ConnectionError:
        return None, "Network error - please check your internet connection"
    except requests.exceptions.Timeout:
        return None, "Request timed out - try again"
    except Exception as err:
        return None, f"An error occurred: {err}"

#Step 3: Extract weather info, including description, icons, humidity, pressure, and wind

def display_weather(data):
    location = data['location']['name']
    country = data['location']['country']
    current = data['current']

    # Weather description and icon URL
    condition = current['condition']['text']
    icon_url = "https:" + current['condition']['icon']

    temp_c = current['temp_c']
    humidity = current['humidity']
    pressure_mb = current['pressure_mb']
    wind_kph = current['wind_kph']
    wind_dir = current['wind_dir']

    print(f"Weather in {location}, {country}:")
    print(f"Condition: {condition}")
    print(f"Temperature: {temp_c} °C")
    print(f"Humidity: {humidity}%")
    print(f"Pressure: {pressure_mb} mb")
    print(f"Wind: {wind_kph} kph from {wind_dir}")
    print(f"Weather Icon URL: {icon_url}")

#Step 4: Handle weather alerts and notifications

def display_alerts(data):
    alerts = data.get('alerts', {}).get('alert', [])
    if alerts:
        print("\nWeather Alerts:")
        for alert in alerts:
            print(f"- {alert['headline']}")
            print(f"  {alert['desc']}")
            print(f"  From: {alert['effective']} To: {alert['expires']}\n")
    else:
        print("\nNo weather alerts currently.")

# Step 5: Putting it all together with error handling and suggestion

def main():
    city = input("Enter the name of the city:\n").strip()

    data, error = get_weather(city)

    if error:
        print("Error:", error)
        # Suggestion for common mistakes (very simple)
        if "HTTP error" in error or "Unexpected response format" in error:
            print("Check if the city name is spelled correctly.")
        return

    # Display weather info
    display_weather(data)

    # Display alerts if any
    display_alerts(data)

    # Optional: Use text-to-speech
    message = f"The current weather in {city} is {data['current']['condition']['text']} with temperature {data['current']['temp_c']} degrees Celsius."
    engine = pyttsx3.init()
    engine.say(message)
    engine.runAndWait()


if __name__ == "__main__":
    main()


