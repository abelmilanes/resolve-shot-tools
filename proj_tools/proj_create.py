import os
import yaml

def create_project(project_name, root_path):
    """Create new project entry in master config and setup folder structure"""
    if not os.path.isdir(root_path):
        print(f"Error: Root path {root_path} does not exist")
        return False

    # Check if project already exists in master config
    master_config_file = 'config/proj_master_config.yaml'
    try:
        with open(master_config_file, 'r') as f:
            master_config = yaml.safe_load(f)

        if 'projects' in master_config:
            for project in master_config['projects']:
                if project_name in project:
                    print(f"Error: Project '{project_name}' already exists in master config")
                    return False

        # Create project directory inside root path
        project_path = os.path.join(root_path, project_name)
        if not os.path.exists(project_path):
            os.makedirs(project_path)
            print(f"Created project directory at {project_path}")

        # Create config directory and copy files
        config_dir = os.path.join( project_path, 'config' )
        os.makedirs(config_dir, exist_ok=True)

        # Copy and modify config.yaml while preserving structure
        example_config = 'config/default_proj_config.yaml'
        new_config = os.path.join( config_dir, 'config.yaml' )
        with open(example_config, 'r') as src:
            lines = src.readlines()

        with open(new_config, 'w') as dst:
            for line in lines:
                if 'name:' in line and 'project' in lines[lines.index(line) - 1]:
                    dst.write(f"  name: {project_name.title()}                   # Project long name\n")
                elif 'alias:' in line and 'project' in lines[lines.index(line) - 2]:
                    dst.write(
                        f"  alias: {project_name.lower()}                  # Project alias for folder structure\n")
                elif 'path:' in line and 'project' in lines[lines.index(line) - 8]:
                    dst.write(
                        f"  path: {project_path}                                # This folder need to be created manually. In this example project path is set to where the rst_gui.py lives\n")
                else:
                    dst.write(line)

        # Add new project to master config
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

        with open(master_config_file, 'w') as f:
            yaml.dump(master_config, f, default_flow_style=False)

        print(f"Created new project '{project_name}' with default configuration")
        return True

    except Exception as e:
        print(f"Error creating project: {e}")
        return False