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

    def __str__(self):
        return f"MockupTask {self.id} - {self.status}"


class MockupImage(models.Model):
    text = models.TextField()
    font = models.CharField(max_length=150, default='roboto')
    color = models.CharField(max_length=150, default='red')
    url = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    task = models.ForeignKey(
        MockupTask, null=True, on_delete=models.SET_NULL, related_name='images')

    def __str__(self):
        return f"MockupImage {self.id} - {self.text[:50]}"