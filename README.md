# resolve-shot-tools
Utility to help with VFX pulls from Davinci Resolve Timelines

## Features
- Creates shot names based on configuration files
- Creates Render jobs for generation of plates for VFX work
- Gnerate shot entris for Kitsu shot management
- YAML based configuration files for shot nameming, metadata, etc

## Requirments
- Python 3.xx
- PySide6
- PyYAML
- numpy
- gazu
- Pillow
- Running Kitsu Server with admin priviledges 


## Usage
- Resolve needs to be running with the relevant timeline opened.
```
python rst_gui.py -p <project name>
```
Example Project
```
python rst_gui.py -p example_project
```
## Configuration
### Config Files
Configuration is currently manual by editing the YAML configuration files in the **config** folder.

Additionally, per project configuration file need to e created and edited. An example project is included in the **example_project** folder.

- Edit the ```./config/proj_master_config.yaml``` file to add you projects
- Edit the ```./config/default_proj_config.yaml``` file to set default parameters for all your projects
- Create and edit per project ```config.yaml``` files to se overrides for specific project parameters. This file should be placed in the ```<project root dir>/config``` folder. An example is provided in the ```./example_project``` folder.

### Resolve Timeline

- In the Resolve Timeline, name the Video Track where the VFX pulls should happen, i.e. ```SRC```
- Edit the configuration file to reflect this in the ```resolve``` section.
```
#Resolve
resolve:
  vfx_plate_trk_name: SRC  
```
- Curently this name will be used to name the rendered plates.

## Notes and Disclaimer 
This project is a HEAVY work in progres and some sections will brake. I am an artist not a developer and the code is far from being efficient. This project is provided as a proof of concept for a more robust tool.
