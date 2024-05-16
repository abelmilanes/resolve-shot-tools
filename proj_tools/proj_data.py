import os
import yaml


# Read master config file
def master_config():
    # A master config file to pull different project config files
    config_file = os.path.join(os.path.dirname(__file__), '../config/proj_master_config.yaml')
    data = {}
    with open(config_file, 'r') as stream:
        try:
            data = (yaml.safe_load(stream))
        except yaml.YAMLError as exc:
            print(exc)
    return data


# Project list
def projects():
    project_list = []
    for proj in master_config()['projects']:
        for param, value in proj.items():
            project_list.append(value['name'])
    return project_list


# Read specific project config
def project_config(project):
    data = {}
    for proj in master_config()['projects']:
        for param, value in proj.items():
            if value['alias'] == project:
                # Project config file should be at the project level
                mtr_data = {param: value}
                def_data = {}
                prj_data = {}
                def_config_file = os.path.join(os.path.dirname(__file__), '../config/default_proj_config.yaml')

                prj_config_file = os.path.join(value['root'], value['alias'], 'config/config.yaml')

                try:
                    if os.path.exists(def_config_file):
                        with open(def_config_file, 'r') as stream1:
                            def_data = (yaml.safe_load(stream1))
                except yaml.YAMLError as exc:
                    print(exc)
                try:
                    if os.path.exists(prj_config_file):
                        with open(prj_config_file, 'r') as stream2:
                            prj_data = (yaml.safe_load(stream2))

                except yaml.YAMLError as exc:
                    print(exc)
                data = {**mtr_data, **def_data, **prj_data}
                if data['project']['path'] == ".":
                    data['project']['path'] = os.getcwd()
    return data


def config():
    project = os.environ['RST_PROJ']
    proj_config = project_config(project)
    return proj_config


if __name__ == "__main__":
    pass
