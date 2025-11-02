import os
from dotenv import load_dotenv
from random import randint
from celery import shared_task , group
from PIL import Image, ImageDraw

load_dotenv()


@shared_task
def create_mockup(text, input_path):
    img = Image.open(input_path)
    painter = ImageDraw.Draw(img)
    painter.text((300, 300), text, fill=(255, 0, 0))
    path_to_save = os.environ.get('GENERATED_IMAGES') + str(randint(1, 1000)) + '.png'
    img.save(path_to_save)
    return 1
