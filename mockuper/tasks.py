from celery import shared_task 
from PIL import Image, ImageDraw


@shared_task
def create_mockup(text, img_path):
    img = Image(img_path)
    painter = ImageDraw.Draw(img)
    painter.text((300, 300), text, fill=(255, 0, 0))
    painter.save('/home/mohammad-yegane-far/programming/Mockuper/created_images')