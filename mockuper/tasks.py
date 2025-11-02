import os
from dotenv import load_dotenv
from random import randint
from celery import shared_task
from PIL import Image, ImageDraw
from mockuper import models

load_dotenv()


@shared_task
def create_mockup(text, input_path, task_id=None):
    img = Image.open(input_path)
    painter = ImageDraw.Draw(img)
    painter.text((300, 300), text, fill=(255, 0, 0))
    file_name = 'generated_image' + str(randint(1, 1000)) + '.png'
    path_to_save = os.environ.get('GENERATED_IMAGES') + file_name
    img.save(path_to_save)
    # save the image to the database
    mockup_image = models.MockupImage.objects.create(
        text=text, url='media/mockups/' + file_name, task_id=task_id)
    return mockup_image.id
