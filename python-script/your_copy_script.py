import json
import os
import shutil
import sys

def load_config(config_path):
    """Load configuration from a JSON file."""
    with open(config_path, 'r') as file:
        config = json.load(file)
    print(f"Configuration loaded from {config_path}")
    return config

# def load_config(config_path):
#     """Load and validate configuration from the specified file."""
#     with open(config_path, 'r') as file:
#         config = json.load(file)
#     if validate_config(config):
#         return config
#     else:
#         raise ValueError("Configuration validation failed")

# def validate_config(config):
#     """Validate and correct the configuration if necessary."""
#     if "operations" not in config:
#         print("Missing 'operations' key. Adding empty operations list.")
#         config['operations'] = []
    
#     for op in config.get('operations', []):
#         required_keys = ['file_name', 'source_directory', 'destination_directory', 'operation']
#         for key in required_keys:
#             if key not in op:
#                 print(f"Missing key '{key}' in operation, setting to default")
#                 if key == 'operation':
#                     op[key] = 'copy'  # Default operation
#                 else:
#                     op[key] = ''  # Default empty string
        
#         if op['operation'] not in ['copy', 'move']:
#             print(f"Invalid operation '{op['operation']}' found, correcting to 'copy'")
#             op['operation'] = 'copy'

#         if not os.path.isabs(op['source_directory']):
#             print(f"Source directory '{op['source_directory']}' is not an absolute path, correcting")
#             op['source_directory'] = os.path.abspath(op['source_directory'])
#         if not os.path.isabs(op['destination_directory']):
#             print(f"Destination directory '{op['destination_directory']}' is not an absolute path, correcting")
#             op['destination_directory'] = os.path.abspath(op['destination_directory'])

#     return True

def process_operations(operations, config_filename):
    """Process each file operation defined in the configuration and include config file name in logs."""
    successes, failures = [], []
    for op in operations:
        file_name = op['file_name']
        src_path = os.path.join(op['source_directory'], file_name)
        dest_path = os.path.join(op['destination_directory'], file_name)
        try:
            if op['operation'] == 'copy':
                shutil.copy(src_path, dest_path)
            elif op['operation'] == 'move':
                shutil.move(src_path, dest_path)
            successes.append(file_name)
        except Exception as e:
            print(f"Failed to [{op['operation']}] {file_name} from {config_filename}: {e}")
            failures.append(file_name)
    return successes, failures

def main(config_path):
    config_filename = os.path.basename(config_path)
    config = load_config(config_path)
    operations = config['operations']
    team_name = config['team_name']
    successes, failures = process_operations(operations, config_filename)
    print(f"Successfully processed: {successes}")
    if failures:
        print(f"Failed to process: {failures},[{team_name}]")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python your_copy_script.py <config_path>")
        sys.exit(1)
    config_path = sys.argv[1]
    main(config_path)
