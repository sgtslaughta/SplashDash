import requests
from PIL import Image, ImageTk
import os


def get_web_image(url="http://someimage.png"):
    """Pull an image from a given URL and set it to a ImageTK.PhotoImage object"""
    img = Image.open(requests.get(url, stream=True).raw)
    cwd = os.getcwd()
    url_fn = url.split('/')
    img.save(f"{cwd}/lib/img/tmp/{url_fn[-1]}")
    image = ImageTk.PhotoImage(img)
    if os.path.exists(f"{cwd}/lib/img/tmp/{url_fn[-1]}"):
        os.remove(f"{cwd}/lib/img/tmp/{url_fn[-1]}")
    return image
