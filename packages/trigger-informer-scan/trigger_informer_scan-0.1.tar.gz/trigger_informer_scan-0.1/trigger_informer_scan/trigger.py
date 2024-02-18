import os
import requests
import argparse
import logging
from uuid import UUID

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def is_valid_uuid(uuid_to_test, version=4):
    try:
        uuid_obj = UUID(uuid_to_test, version=version)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_to_test

def post_uuid(uuid):
    if not is_valid_uuid(uuid):
        logging.error("The UUID provided is invalid")
        return

    url = "https://api.informer.io/trigger"
    data = {"uuid": uuid}
    timeout = 10  # seconds

    try:
        response = requests.post(url, json=data, timeout=timeout)
        response.raise_for_status()
        logging.info(f"Request to Informer.io to trigger a scan was successful: {response.json()}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Request to Informer.io to trigger a scan failed: {e}")

def main():
    parser = argparse.ArgumentParser(description='Trigger a scan in Informer.io')
    parser.add_argument('-u', '--uuid', type=str, help='UUID to post')
    args = parser.parse_args()

    uuid = args.uuid if args.uuid else os.getenv('INFORMER_TEST_UUID')

    if not uuid:
        logging.error("No UUID provided. Please provide it as an argument or set 'INFORMER_TEST_UUID' environment variable.")
    else:
        post_uuid(uuid)

if __name__ == "__main__":
    main()
