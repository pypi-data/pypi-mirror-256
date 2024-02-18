# Example Python Project
This repository represents the bare minimum required to create a python package that can be distributed.
## Key Files
| File  | Purpose |
| ------------- | ------------- |
| setup.py  | Contains all the metadata and how to build the code artifact. Setup.py usually contains the author, email, name and version of the package. A full list of what can be saved in a setup.py is [available here](https://docs.python.org/3.11/distutils/setupscript.html) |
| requirements.txt  | The external dependencies. In order for this project to run, it needs to download OTHER projects and use them. |
| README.md  | This project description document |
| src dir  | The directory labeled "src" contains all the Python modules. This setup.py will iterate this file to find the modules  |
| scripts dir  | The directory labeled "scripts" contains all command-line executable programs provided by the project |
## PyPi
This project has been published to PyPi as an example. This can be found here.

## Installation
Installing this project from pypi is done with this command

```cmd
pip install csc_cyb600_jmdv
```
