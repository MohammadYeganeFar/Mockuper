from django.db import models

class MockupTask(models.Model):
    STATUS_CHOICES = {
        'PENDING': 'Pending',
        'STARTED': 'Started',
        'RETRY': 'Retry',
        'FAILURE': 'Failure',
        'SUCCESS': 'Success' 
    }
    task_uuid = models.UUIDField(null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')


class MockupImage(models.Model):
    text = models.TextField()
    url = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    task = models.ForeignKey(
        MockupTask, null=True,on_delete=models.SET_NULL, related_name='images')