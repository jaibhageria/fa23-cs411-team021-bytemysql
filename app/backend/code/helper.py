import requests
import binascii
import base64

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