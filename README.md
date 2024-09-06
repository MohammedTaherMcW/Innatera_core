# Innatera Core
Innatera core is the Backend for the Extension which supports various functionalities such as creation of project, manage, test, debug.

# Installation Guide

## 1) Clone the Repository
#### Run the below command to clone the Innatera Core Repository

``` 
git clone https://github.com/MohammedTaherMcW/Innatera_core.git 
```

## 2) Create a virtual Environment

#### Create a virtual Environment using the below command
```
python3 -m venv innatera_core
```
## 3) Activate the Virtual Environment

#### To activate the virtual environment
 ```
source innatera_core/bin/activate
 ```
## 4) Install the Innatera Core

#### Run the below command to install the Innatera core in the Virtual Environment
```
pip install .
```

## 5) Verify the Installaton of the Innatera Core
* Activate the Environment  
```
source innatera_core/bin/activate
```

* Use the below command to verify the installtion of the Innatera Core  

 ```
~/.platformio/penv/bin/pio -h
```

# Usage

* Activate the Environment  
```
source innatera_core/bin/activate
```  

#### Use the help command to list down the commands available in the PIO and to check the usage of the commands  
```
pio -h
```

Example:  
```bash
pio -h
Usage: pio [OPTIONS] COMMAND [ARGS]...

Options:
  --version          Show the version and exit.
  -c, --caller TEXT  Caller ID (service)
  --no-ansi          Do not print ANSI control characters
  -h, --help         Show this message and exit.

Commands:
  access    Manage resource access
  account   Manage PlatformIO account
  boards    Board Explorer
  check     Static Code Analysis
  ci        Continuous Integration
  custom    GUI to manage PlatformIO
  debug     Unified Debugger
  device    Device manager & Serial/Socket monitor
  home      GUI to manage PlatformIO
  org       Manage organizations
  pkg       Unified Package Manager
  project   Project Manager
  remote    Remote Development
  run       Run project targets (build, upload, clean, etc.)
  settings  Manage system settings
  system    Miscellaneous system commands
  team      Manage organization teams
  test      Unit Testing
  upgrade   Upgrade PlatformIO Core to the latest version


pio project init
Project has been successfully updated!

```
