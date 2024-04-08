import subprocess
import os
from tqdm import tqdm
import logging

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create handlers
success_handler = logging.FileHandler('../Logging/upload_success.log')
error_handler = logging.FileHandler('../Logging/upload_error.log')
console_handler = logging.StreamHandler()  # Terminal output

# Create formatters and add it to handlers
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
success_handler.setFormatter(formatter)
error_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Set level for handlers
success_handler.setLevel(logging.INFO)
error_handler.setLevel(logging.ERROR)
console_handler.setLevel(logging.INFO)

# Add handlers to the logger
logger.addHandler(success_handler)
logger.addHandler(error_handler)
logger.addHandler(console_handler)

# Base directory where the JSON files are stored
base_dir = '../../Hospital Price Transparency Data'


def find_json_files(directory):
    """Generator function to find all JSON files within the directory and its subdirectories."""
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                yield os.path.join(root, file)


def upload_json_to_redis(file_path):
    """Use subprocess to call redis-cli and upload JSON file content to Redis."""
    redis_key = file_path.replace('/', ':').replace(' ', '_').replace(base_dir, '').lstrip(':')
    command = ['redis-cli', '-x', 'JSON.SET', redis_key, '.']
    with open(file_path, 'rb') as file:  # Open as binary
        try:
            result = subprocess.run(command, input=file.read(), check=True, capture_output=True)
            logger.info(f"Successfully uploaded {file_path}")
            print(f"Success: {file_path}")  # Terminal output for success
        except subprocess.CalledProcessError as e:
            error_message = e.stderr.decode('utf-8') if e.stderr else 'Unknown error'
            logger.error(f"Failed to upload {file_path}. Error: {error_message}")
            print(f"Error: {file_path}")  # Terminal output for failure


def main():
    json_files = list(find_json_files(base_dir))
    progress_bar = tqdm(total=len(json_files), desc="Uploading files to Redis", unit="file")

    for file_path in json_files:
        upload_json_to_redis(file_path)
        progress_bar.update(1)

    progress_bar.close()


if __name__ == "__main__":
    main()
