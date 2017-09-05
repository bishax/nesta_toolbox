# `example`:
An example of a snippet which might be used by others.

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

     # Get and print London wind speeds
     w = get_london_weather()
     print(w.get_wind())

Note that object `w` is described in the module [pyowm](https://github.com/csparpa/pyowm).

