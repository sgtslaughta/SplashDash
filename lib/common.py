import requests
from PIL import Image, ImageTk
import os
import matplotlib.pyplot as plt


def sv_rm_file(file, img):
    if not os.path.exists('lib/img/tmp'):
        os.mkdir('lib/img/tmp')
    img.save(f'lib/img/tmp/{file}')
    img = ImageTk.PhotoImage(img)
    if os.path.exists(f'lib/img/tmp/{file}'):
        os.remove(f'lib/img/tmp/{file}')
    return img


def get_web_image(url="http://someimage.png"):
    """Pull an image from a given URL and set it to a ImageTK.PhotoImage object"""
    img = Image.open(requests.get(url, stream=True).raw)
    url_fn = url.split('/')
    image = sv_rm_file(f"{url_fn[-1]}", img)
    return image


def get_web_image_resize(hgt, wdth, url="http://someimage.png"):
    img = Image.open(requests.get(url, stream=True).raw)
    img = img.resize((int(img.height/hgt), int(img.width/wdth)), Image.ANTIALIAS)
    return ImageTk.PhotoImage(img)


def make_graph_of_size(clr1='red', clr2='green', hlst=(), tlst=(), scale=0):
    plt.rcParams.update({'font.size': 7})
    plt.rcParams.update({'text.color': clr2})

    plt.figure(figsize=(6, 2), dpi=600)
    plt.axis('off')
    plt.plot(hlst, tlst, color=clr1)

    for t, j in zip(hlst, tlst):
        plt.annotate(str(j), xy=(t, j+.2))

    plt.savefig('lib/img/tmp/test.png', bbox_inches='tight', transparent=True)
    plt.close('all')

    img = Image.open('lib/img/tmp/test.png')
    width, height = img.size
    ratio = int(width / scale)
    if not os.path.exists('lib/img/tmp'):
        os.mkdir('lib/img/tmp')
    img = img.resize((int(scale), int(height / ratio) - 40), Image.ANTIALIAS)
    if os.path.exists('lib/img/tmp/test.png'):
        os.remove('lib/img/tmp/test.png')
    return ImageTk.PhotoImage(img)
    # print(tlst, hlst)
    # fig = plt.figure()
    # #plt.yticks(range(int(min(tlst) - 10), int(max(tlst) + 10)))
    # #ax = fig.add_subplot(111)
    # fig.plot(tlst, color=clr)
    # fig.savefig('test.png', bbox_inches='tight', transparent=True)


    # lst = plt.plot(lst)
    # plt.axis('off')
    # plt.savefig('test.png', bbox_inches='tight', transparent=True)
