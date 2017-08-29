'''
example

This is an example of a python module. It contains all the required elements
for being promoted to nesta-toolbox.official.modules.

The specific example here simply demonstrates how to check the weather in London,
with the API key read from an configuration file.
'''

import requests
import configparser

class WeatherChecker(configparser.ConfigParser):
    '''
    Basic class to check weather at a given place. The class inherits from
    ConfigParser, and expects to find a file api.config containing a variable
    DEFAULT.API_KEY. Basic usage:
    
        wc = WeatherChecker()
        wc.get_weather_at_place("Some place name")
    '''
    def __init__(self):
        '''
        Wrapper to ConfigParser, to read config file and store 
        the parameters in self
        '''
        # Read the config file
        super().__init__()
        self.read('api.config')
        # Make sure that the file exists & contains the relevant info
        try:
            self["DEFAULT"]["API_KEY"]
        except KeyError as err:
            raise KeyError("Couldn't find DEFAULT.API_KEY variable in a "
                           "file api.config in this directory.")
        
    def get_weather_at_place(self,place):
        '''
        A wrapper to the OpenWeatherMap API.
        
        :param place: the query string for OpenWeatherMap
        :type place: str
        '''
        url="http://api.openweathermap.org/data/2.5/weather"
        params=dict(q=place,appid=self["DEFAULT"]["API_KEY"])
        r = requests.get(url,params)
        r.raise_for_status()
        return r.json()
        
# Write an example main routine in a __name__ == __main__ snippet
if __name__ == "__main__":
    # Get and print London wind speeds
    wc = WeatherChecker()
    weather = wc.get_weather_at_place("London,UK")
    print(weather)
