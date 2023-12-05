import requests
import binascii
import base64
import logging
import sys

# Configure the logging module
logging.basicConfig(
    stream=sys.stdout,  # Log to standard output
    level=logging.ERROR,  # Set the logging level to ERROR or higher
    format='%(asctime)s [%(levelname)s] - %(message)s',  # Define the log message format
    datefmt='%Y-%m-%d %H:%M:%S'  # Define the date and time format
)

# Function to fetch a random user image from the Random User Generator API and convert it to hex
def fetch_random_user_image():
    response = requests.get("https://randomuser.me/api/")
    user_data = response.json()
    image_url = user_data["results"][0]["picture"]["large"]
    image_response = requests.get(image_url)
    image_bytes = image_response.content
    image_hex = binascii.hexlify(image_bytes).decode("utf-8")
    return image_hex

def base64_encode_picture(picture):
    if picture:
        return base64.b64encode(picture).decode('utf-8')
    return None

def debug(s):
    logging.debug('{0}'.format(s))
    sys.stdout.flush()

def info(s):
    logging.info('{0}'.format(s))
    sys.stdout.flush()

def error(s):
    logging.error('{0}'.format(s))
    sys.stdout.flush()
