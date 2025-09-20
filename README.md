# resolve-shot-tools
Utility to help with VFX pulls from Davinci Resolve Timelines

Tested on Rocky Linux 9.3, Resolve 20.2, Kitsu 0.20.87, Python 3.11.

![rst_gui_screenshot.png](docs/rst_gui_screenshot.png)

# Quick Start
https://vimeo.com/952901264

## Features
- Creates shot names from current Davinci Resolve Timeline.
- Creates Render jobs for generation of plates for VFX work.
- Generates shot entries for Kitsu shot management.
- YAML based configuration files for shot naming, metadata, etc.
- **NEW!** Timeline Clip Name used for shot naming.
- **NEW!** Flag for creating a project config file given a project root dir.

## Requirments
### Python
- Python 3.xx
- PySide6
- PyYAML
- numpy
- gazu
- Pillow

### Software
- Davinci Resolve
- Running Kitsu Server with admin priviledges 

## Usage
- Resolve needs to be running with the relevant timeline opened.

```
usage: rst_gui.py [-h] [-p PROJECT] [-C PROJECT_PATH]

Tools to help with VFX shot work in DaVinci Resolve

options:
  -h, --help            show this help message and exit
  -p PROJECT, --project PROJECT
                        VFX Project name
  -C PROJECT_PATH, --create PROJECT_PATH
                        Create new project at specified root path
```
```
python rst_gui.py -p <project name>
```
Included Example Project
```
python rst_gui.py -p example_project
```
## Configuration
### Resolve Python API
- Edit ```./resolve_tools/resolve_connect.py``` to point to your Resolve installation Resolve Python API modules.
### Environment Variables
If the ```RST_CONFIG_DIR``` environment variable is set, the application will look for the configuration files in that path. If not set, it will look in the ```./config/``` folder relative to where the application is run from.
### Config Files
- ```./config/proj_master_config.yaml``` or ```$RST_CONFIG_DIR/proj_master_config.yaml``` Created projects. Proects will be added automatically by the -```--create <PROJECT_PATH>``` option.
- ```./config/default_proj_config.yaml``` or  ```$RST_CONFIG_DIR/default_proj_config.yaml```Config files with default parameters for all created projects.
- ```<project root dir>/config/config.yaml``` Per project configuration file. Created manually or by the ```--create <PROJECT_PATH>``` option. Any setting set at the project level ```config.yaml``` file overrides the same setting on the ```default_proj_config.yaml```.

### Adding Sequences
- VFX sequences can be added in the ```sequences``` section of the configurations file. This shoudl be done is the project level ```config.yaml``` file.
```
  sequences:
    - seq01
    - seq02
    - seq03
```

### Resolve Timeline

- In the Resolve Timeline, name the Video Track where the VFX pulls should happen, i.e. ```SRC```
- Edit the configuration file to reflect this in the ```resolve``` section.
```
#Resolve
resolve:
  vfx_plate_trk_name: SRC  
```
- Curently this name is used to name the rendered plates. This can be changed in Naming section of the project configuration file.

### Kitsu
A Kitsu Project needs to be present. The project name should be mirrored in the ```proj_master_config.yaml``` file.

Kitsu Server URL can be edited in the configuration files. You need administrative credentials to publish Kitsu shot entries. The creadential are read from the following System Environment Variables:
```
TX_KITSU_ADMIN = username
TX_KITSU_PASWD = password
```
In addition, valid Task and Status entries need to be defined in the Kitsu Project. These need to match the ones set in the Kistu section of the configuration files.
```commandline
kitsu:
  shot_create_task: Comp                  # This need to be a valid task name in Kitsu
  shot_create_status: RTS                 # Ready to start. This need to be a valid status name in Kitsu
```

## Notes and Disclaimer 
This project is a HEAVY work in progres and some sections will brake. I am an artist not a developer and the code is far from being efficient. This project is provided as a proof of concept for a more robust tool.
