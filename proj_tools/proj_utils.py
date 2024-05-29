import sys
import yaml
import os
from proj_tools.proj_data import Config


class ProjectUtils:
    def __init__(self):
        config = Config().get_config()
        self.proj_path = config['project']['path']
        self.proj_alias = config['project']['alias']

    def mk_tree(self, level_path, preset, app='', dry_run=False):
        """Create folder structures based on presets from YAML definitions."""
        fs_file = os.path.join(self.proj_path, self.proj_alias, "config", "folder_structure.yaml")
        if not os.path.exists(fs_file):
            fs_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../config/folder_structure.yaml")

        try:
            with open(fs_file, 'r') as stream:
                structure = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print("Error loading folder structure YAML:", exc)
            return

        mkdir_presets = structure.get('presets', {})
        preset_folders = mkdir_presets.get(preset, {}).get('folders', [])
        folder_list = set()

        for folder in preset_folders:
            folder_name = folder['name']
            folder_path = os.path.join(level_path, folder_name)
            folder_create = folder.get('default', False)
            if folder_name == app:
                folder_create = True
            if folder_create:
                folder_list.add(folder_path)
                print("Created:", folder_path)
                for sub_folder in folder.get('folders', []):
                    sub_folder_name = sub_folder['name']
                    sub_folder_path = os.path.join(folder_path, sub_folder_name)
                    sub_folder_create = sub_folder.get('default', False)
                    if sub_folder_create:
                        folder_list.add(sub_folder_path)
                        print("Created:", sub_folder_path)
                    else:
                        print("Not created:", sub_folder_path)
            else:
                print("Not created:", folder_path)

        if not dry_run:
            for p in sorted(folder_list):
                self.mk_dir(p)

    def mk_dir(self, dpath, dry_run=False):
        """Create a directory if it doesn't already exist."""
        if not os.path.exists(dpath):
            try:
                if not dry_run:
                    os.makedirs(dpath)
                else:
                    print('dryrun')
                print("Created:", dpath)
            except Exception as ex:
                print("Error creating directory:", ex)
        else:
            print("Folder already exists:", dpath)

    @staticmethod
    def message(string):
        """Print a message to stdout."""
        sys.stdout.write(string)
        sys.stdout.flush()

# Example usage:
# proj_utils = ProjectUtils()
# proj_utils.mk_tree('/path/to/level', 'preset_name', 'app_name')
