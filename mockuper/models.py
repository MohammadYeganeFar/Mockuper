from django.db import models


class MockupImage(models.Model):
    text = models.TextField()
    image = models.ImageField(upload_to='mockup_images')
    created_at = models.DateTimeField(auto_now_add=True)