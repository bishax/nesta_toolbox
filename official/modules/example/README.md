# `example`:
An example of a module which might be used by others.

## Modules
### `example`
#### Sign-off status
Signed off by: Joel

|  Procedure | Status |
| --- | --- | 
| Docstrings for every exposable method | Yes  | 
| Docstrings for every editable parameter, near the top of the file | Yes
| Docstring at the of the top file | Yes |
| CamelCase class names | Yes |
| Underscore separation of all other variable, function and module names | Yes |
| Usage in this README or in Docstring at the top of the file  | Yes |
| A requirements file* | Yes |
| Successful hallway testing | Yes |

\* Note that you can generate a requirements file according to **Method 2** [here](http://www.idiotinside.com/2015/05/10/python-auto-generate-requirements-txt/).
#### Usage

     # Get and print London weather
     wc = WeatherChecker()
     weather = wc.get_weather_at_place("London,UK")
     print(weather)

