import os
from dotenv import load_dotenv
from random import randint
from logging import getLogger
from celery import shared_task
from celery.signals import task_failure, task_success
from PIL import Image, ImageDraw
from django.core.exceptions import ObjectDoesNotExist
from mockuper import models

load_dotenv()
logger = getLogger(__name__)


@shared_task
def create_mockup(text, input_path, task_id=None):
    """Create a mockup image by overlaying text on an input image."""
    try:
        img = Image.open(input_path)
        painter = ImageDraw.Draw(img)
        painter.text((300, 300), text, fill=(255, 0, 0))
        
        file_name = f'generated_image{randint(1, 1000)}.png'
        base_path = os.environ.get('GENERATED_IMAGES', '')
        path_to_save = os.path.join(base_path, file_name) if base_path else file_name
        
        os.makedirs(os.path.dirname(path_to_save) if os.path.dirname(path_to_save) else '.', exist_ok=True)
        img.save(path_to_save)

        media_url_prefix = os.environ.get('MEDIA_URL_PREFIX', '')
        image_url = os.path.join(media_url_prefix, file_name) if media_url_prefix else file_name
        
        models.MockupImage.objects.create(
            text=text,
            url=image_url,
            task_id=task_id
        )
        
        return task_id
    except Exception as e:
        logger.error(f"Error creating mockup: {str(e)}", exc_info=True)
        raise


@task_success.connect(sender=create_mockup)
def task_success_notifier(**kwargs):
    task = models.MockupTask.objects.get(id=kwargs['result'])
    task.status = 'SUCCESS'
    task.save()

@task_failure.connect(sender=create_mockup)
def task_failure_notifier(**kwargs):
    task = models.MockupTask.objects.get(id=kwargs['result'])
    task.status = 'FAILURE'
    task.save()

