from django.db import models


class MockupImage(models.Model):
    text = models.TextField()
    url = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)