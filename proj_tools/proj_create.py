import os
import yaml
from typing import Tuple, Optional, Dict, Any
from proj_tools.proj_data import MASTER_CONFIG_FILE, DEFAULT_CONFIG_FILE

class ProjectCreator:
    def __init__(self):
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.main_dir = os.path.dirname(self.current_dir)
        self.master_config_file = MASTER_CONFIG_FILE
        self.default_config = DEFAULT_CONFIG_FILE

    def create_project_folder(self, root_path: str, project_name: str) -> Optional[str]:
        """Create project directory inside root path"""
        try:
            if not os.path.isdir(root_path):
                raise ValueError(f"Root path {root_path} does not exist")

            project_path = os.path.join(root_path, project_name)
            if not os.path.exists(project_path):
                os.makedirs(project_path)
                print(f"Created project directory at {project_path}")
            return project_path
        except Exception as e:
            print(f"Error creating project folder: {e}")
            return None

    def create_config(self, project_path: str, project_name: str) -> bool:
        """Create and setup project config file"""
        try:
            config_dir = os.path.join(project_path, 'config')
            os.makedirs(config_dir, exist_ok=True)
            new_config = os.path.join(config_dir, 'config.yaml')

            with open(self.default_config, 'r') as src:
                lines = src.readlines()

            with open(new_config, 'w') as dst:
                for line in lines:
                    if 'name:' in line and 'project' in lines[lines.index(line) - 1]:
                        dst.write(f"  name: {project_name.title()}                   # Project long name\n")
                    elif 'alias:' in line and 'project' in lines[lines.index(line) - 2]:
                        dst.write(f"  alias: {project_name.lower()}                  # Project alias for folder structure\n")
                    elif 'path:' in line and 'project' in lines[lines.index(line) - 8]:
                        dst.write(f"  path: {project_path}                           # Project path\n")
                    else:
                        dst.write(line)
            print(f"Created config file: {new_config}")
            return True
        except Exception as e:
            print(f"Error creating config: {e}")
            return False

    def update_master_config(self, project_name: str, root_path: str) -> bool:
        """Update master config with new project"""
        try:
            with open(self.master_config_file, 'r') as f:
                master_config = yaml.safe_load(f) or {}

            new_project = {
                project_name: {
                    'name': project_name.title(),
                    'alias': project_name.lower(),
                    'root': root_path
                }
            }

            if 'projects' not in master_config:
                master_config['projects'] = []
            master_config['projects'].append(new_project)

            with open(self.master_config_file, 'w') as f:
                yaml.dump(master_config, f, default_flow_style=False)
            return True
        except Exception as e:
            print(f"Error updating master config: {e}")
            return False

    def check_project_exists(self, project_name: str) -> bool:
        """Check if project exists in master config"""
        try:
            with open(self.master_config_file, 'r') as f:
                master_config = yaml.safe_load(f)

            if 'projects' in master_config:
                return any(project_name in project for project in master_config['projects'])
            return False
        except Exception:
            return False

    def create_project(self, project_name: str, root_path: str) -> bool:
        """Main method to create new project"""
        try:
            # Check if project already exists in master config

            if self.check_project_exists(project_name):
                # Get project path from master config
                with open(self.master_config_file, 'r') as f:
                    master_config = yaml.safe_load(f)
                    for project in master_config['projects']:
                        if project_name in project:
                            # If config doesn't exists, create it
                            project_path = os.path.join(project[project_name]['root'], project_name)
                            config_path = os.path.join(project_path, 'config', 'config.yaml')
                            if os.path.exists(project_path) and os.path.exists(config_path):
                                return True

                            if not os.path.exists(config_path):
                                return self.create_config(project_path, project_name)
                            return True
                return False

            # For new projects, continue with normal creation flow
            project_path = self.create_project_folder(root_path, project_name)
            if not project_path:
                return False

            if not self.create_config(project_path, project_name):
                return False

            if not self.update_master_config(project_name, root_path):
                return False

            print(f"Created new project '{project_name}' with default configuration")
            return True

        except Exception as e:
            print(f"Error creating project: {e}")
            return False
