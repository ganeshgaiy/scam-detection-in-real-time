from PIL import Image
import pytesseract as pts
import requests

def download_image(image_url, save_path):
    response = requests.get(image_url, stream=True)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
    else:
        print(f"Failed to download image: {response}")

def extract_text_from_image(image_path):
    image = Image.open(image_path)
    text = pts.image_to_string(image)
    return text







