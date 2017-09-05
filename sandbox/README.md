# Sandbox

This is an area for staging Nesta code snippets and modules.

A note for external users: don't rely on any code committed here. Please
go to `nesta-toolbox.official`.

A note for the Nesta team: please don't commit any API keys or large files
here. 

## Getting your code promoted to Official

### Snippets and Modules

There are two types of "Official" Nesta code: "Snippets" and "Modules".
There is clearly no well-defined split between the two concepts, however
Snippets are generally short pieces of code that serve as examples
of how to do something, whereas Modules demonstrate extensive, efficient
and (most importantly) general functionality.

## Examples

A good example of a Snippet candidate can be found `jaklinger.microsoft_academic_knowledge`,
which could be promoted to a module if the functionality is sufficiently generalised. A
bad example of a Snippet can be found in `example.is_number`, which is a highly specific
piece of code.

## Sign-off

In order to promote your own code to Official, it needs to be "signed off". For this, you need to be
able to fill out the following table for each module of code:

|  Procedure | Status |
| --- | --- |
| Docstrings for every exposable method | No |
| Docstrings for every editable parameter, near the top of the file | No |
| Docstring at the of the top file | No |
| CamelCase class names | No |
| Underscore separation of all other variable, function and module names | No |
| Usage in this README or in Docstring at the top of the file  | No |
| A requirements file* | No |
| Successful hallway testing | No |

\* Note that you can generate a requirements file according to **Method 2** [here](http://www.idiotinside.com/2015/05/10/python-auto-generate-requirements.txt).
