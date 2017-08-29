'''
example

This is an example of a python code snippet. It contains all the required elements
for being promoted to nesta-toolbox.official.snippets.

The specific example here simply demonstrates how check the weather in London. 
'''

# Give a brief description of obscure imports. This is for OpenWeatherMap.
import pyowm

# Any dodgy constants here (note that this wouldn't be tolerated in a module!)
API_KEY = "7ed98818e23b42e5349d814873a59b87" # Get this from https://home.openweathermap.org/api_keys

# Always write a docstring for your functions describing functionality
'''Get weather data for London'''
def get_london_weather():
    owm = pyowm.OWM(API_KEY)
    observation = owm.weather_at_place('London,uk')
    w = observation.get_weather()
    return w

# Write your main routine in a __name__ == __main__ snippet
if __name__ == "__main__":
    # Get and print London wind speeds
    w = get_london_weather()
    print(w.get_wind())
