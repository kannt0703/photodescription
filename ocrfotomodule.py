import pytesseract
from flask import request
import requests
import shutil
from PIL import Image
import os


pytesseract.pytesseract.tesseract_cmd = '/app/vendor/tesseract-ocr/bin/tesseract'

def get_ocr(url):
    filename = url.split("/")[-1]
    response = requests.get(url, stream=True)
    with open(str(filename), 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    img = Image.open(filename)
    new_size = tuple(4*x for x in img.size)
    img = img.resize(new_size, Image.ANTIALIAS)
    img.save("4x"+filename)
    text = pytesseract.image_to_string(Image.open("4x"+filename), lang='rus')
    text = text.replace("\n\n","\n")
    os.remove(filename)
    os.remove("4x"+filename)
    return text


if __name__ == "__main__":
    # photo_url = "https://sun9-65.userapi.com/c205824/v205824047/b9c81/vCUPkGQFt20.jpg"
    # result = get_ocr(photo_url)
    print("only for heroku")
