import sys
import yaml
import os
from proj_tools.proj_data import config


# Creates folder structures based in presets from json definitions
def mk_tree(level_path, preset, app='', dry_run=False):
    # Read folder structure file
    proj_path = config()['project']['path']
    proj = config()['project']['alias']
    fs_file = os.path.join(proj_path, proj, "config", "folder_structure.yaml")
    if not os.path.exists(fs_file):
        fs_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../config/folder_structure.yaml")
    with open(fs_file, 'r') as stream:
        try:
            structure = (yaml.safe_load(stream))
        except yaml.YAMLError as exc:
            print(exc)
    mkdir_presets = structure['presets']
    folder_list = set()
    preset_folders = mkdir_presets[preset]['folders']
    for folder in preset_folders:
        folder_name = folder['name']
        folder_path = os.path.join(level_path, folder_name)
        folder_create = folder['default']
        if folder_name == app:
            folder_create = True
        if folder_create:
            folder_list.add(folder_path)
            print("Created: ", folder_path)
            try:
                if folder['folders']:
                    for sub_folder in folder['folders']:
                        sub_folder_name = sub_folder['name']
                        sub_folder_path = os.path.join( folder_path, sub_folder_name )
                        sub_folder_create = sub_folder['default']
                        if sub_folder_create:
                            folder_list.add(sub_folder_path)
                            print("Created: ", sub_folder_path)
                        else:
                            print("Not created: ", sub_folder_path)
            except Exception as ax:
                print("No: ", ax)
                pass
        else:
            print("Not created: ", folder_path)
    print(folder_list)
    if not dry_run:
        for p in sorted(folder_list):
            mk_dir(p)


def mk_dir(dpath, dry_run=False):
    if not os.path.exists(dpath):
        try:
            if not dry_run:
                os.makedirs(dpath)
            else:
                print('dryrun')
            print("%s: %s" % ('Created', dpath))
        except Exception as ex:
            print(ex)
    else:
        print("%s: %s" % ('Folder already exists', dpath))


def message(string):
    sys.stdout.write(string)
    # sys.stdout.flush()


if __name__ == "__main__":
    pass
