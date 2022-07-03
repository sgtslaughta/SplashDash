import requests
from PIL import Image, ImageTk
from io import BytesIO


def get_web_image(url):
    u = requests.get(url)
    image = ImageTk.PhotoImage(Image.open(BytesIO(u.content)))
    return image
