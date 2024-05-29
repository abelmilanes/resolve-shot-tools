import os
import yaml


class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._config = cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        project_alias = os.getenv('RST_PROJ')
        if not project_alias:
            raise ValueError("Project alias must be provided or set in the environment variable 'RST_PROJ'.")
        return project_config(project_alias)

    def get_config(self):
        return self._config


CONFIG_DIR = os.path.join(os.path.dirname(__file__), '../config')
MASTER_CONFIG_FILE = os.path.join(CONFIG_DIR, 'proj_master_config.yaml')
DEFAULT_CONFIG_FILE = os.path.join(CONFIG_DIR, 'default_proj_config.yaml')


def load_yaml(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return {}
    with open(file_path, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(f"Error loading YAML file: {file_path}\n{exc}")
            return {}


def master_config():
    return load_yaml(MASTER_CONFIG_FILE)


def projects():
    return [proj[next(iter(proj))]['name'] for proj in master_config().get('projects', [])]


def deep_merge_dicts(source, destination):
    for key, value in source.items():
        if isinstance(value, dict):
            node = destination.setdefault(key, {})
            deep_merge_dicts(value, node)
        else:
            destination[key] = value
    return destination


def project_config(project_alias):
    config_data = {}
    master_data = master_config()
    for proj in master_data.get('projects', []):
        for param, value in proj.items():
            if value['alias'] == project_alias:
                master_data = {param: value}
                default_data = load_yaml(DEFAULT_CONFIG_FILE)
                project_config_file = os.path.join(value['root'], value['alias'], 'config/config.yaml')
                project_data = load_yaml(project_config_file)

                config_data = deep_merge_dicts(default_data, master_data)
                config_data = deep_merge_dicts(project_data, config_data)

                if config_data['project']['path'] == ".":
                    config_data['project']['path'] = os.getcwd()
                break
    return config_data


def config(project_alias=None):
    if project_alias is None:
        project_alias = os.getenv('RST_PROJ')
    if not project_alias:
        raise ValueError("Project alias must be provided or set in the environment variable 'RST_PROJ'.")
    return project_config(project_alias)
