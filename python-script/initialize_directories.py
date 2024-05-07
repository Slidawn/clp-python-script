# initialize_directories.py
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

def collect_unique_directories(config):
    """Collect all unique destination directories from the operations."""
    unique_dirs = set()
    for op in config['operations']:
        unique_dirs.add(op['destination_directory'])
    print(f"Collected {len(unique_dirs)} unique destination directories.")
    return unique_dirs

def initialize_directory(directory_path):
    """Clear existing directory or create if it does not exist."""
    if os.path.exists(directory_path):
        print(f"Directory {directory_path} exists. Clearing contents...")
        shutil.rmtree(directory_path)
    else:
        print(f"Directory {directory_path} does not exist. Creating...")
    os.makedirs(directory_path, exist_ok=True)
    print(f"Directory {directory_path} has been initialized.")

def main(config_path):
    config = load_config(config_path)
    unique_dirs = collect_unique_directories(config)
    for directory_path in unique_dirs:
        initialize_directory(directory_path)
    print("All unique directories have been initialized successfully.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python initialize_directories.py <config_path>")
        sys.exit(1)
    config_path = sys.argv[1]
    main(config_path)
