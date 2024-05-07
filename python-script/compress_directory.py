# compress_directory.py
import json
import tarfile
import sys
import os

def load_config(config_path):
    """Load configuration from a JSON file."""
    with open(config_path, 'r') as file:
        return json.load(file)

def compress_directories(unique_dirs, compression_path):
    """Compress each unique destination directory to the designated compression folder."""
    for dest_dir in unique_dirs:
        # Construct the path for the tar.gz file
        tar_path = os.path.join(compression_path, f"{os.path.basename(dest_dir)}.tar.gz")
        with tarfile.open(tar_path, "w:gz") as tar:
            tar.add(dest_dir, arcname=os.path.basename(dest_dir))
            print(f"Directory {dest_dir} compressed to {tar_path}")

def collect_unique_directories(config):
    """Collect all unique destination directories from the operations."""
    unique_dirs = set()
    for op in config['operations']:
        dest_dir = op['destination_directory']
        unique_dirs.add(dest_dir)
    return unique_dirs

def main(config_path):
    config = load_config(config_path)
    unique_dirs = collect_unique_directories(config)
    compression_path = config.get('compression_destination', os.path.dirname(__file__))  # Use a default if not specified
    if not os.path.exists(compression_path):
        os.makedirs(compression_path)

    compress_directories(unique_dirs, compression_path)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python compress_directory.py <config_path>")
        sys.exit(1)
    config_path = sys.argv[1]
    main(config_path)
