from django.db import models

class MockupTask(models.Model):
    STATUS_CHOICES = {
        'PENDING': 'Pending',
        'STARTED': 'Started',
        'RETRY': 'Retry',
        'FAILURE': 'Failure',
        'SUCCESS': 'Success' 
    }
    task_id = models.UUIDField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)


class MockupImage(models.Model):
    text = models.TextField()
    url = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)