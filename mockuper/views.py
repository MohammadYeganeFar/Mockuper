import os
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from celery import group
from celery.result import AsyncResult
from mockuper import serializers
from mockuper import tasks
from mockuper import models


@api_view(['POST'])
def generate_mockup_shirt(request):
    # Serializing the data
    serializer = serializers.MockupImageSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    text = request.data['text']

    # Creating the tasks
    files = os.listdir('mockuper/shirt_images')
    images_abs_path = [os.environ.get('SAMPLE_IMAGES') + file for file in files]

    # Saving the task to the database
    task = models.MockupTask.objects.create()

    # Creating the tasks signatures
    tasks_signatures = [tasks.create_mockup.s(text, path, task.id) for path in images_abs_path]
    # Creating the multiple mockup tasks
    multiple_mockup_tasks = group(tasks_signatures)
    # Executing the tasks
    executed_tasks = multiple_mockup_tasks.delay()

    task.task_uuid = executed_tasks.id
    res = AsyncResult(executed_tasks.id)
    task.status = res.state
    task.save()
    data = {
        'task_uuid': executed_tasks.id,
        'status': res.state,
        'message': 'ساخت تصویر آغاز شد'
    }
    return Response(data, status.HTTP_201_CREATED)

@api_view(['GET'])
def get_task_status(request, task_uuid):
    task = get_object_or_404(models.MockupTask, task_uuid=task_uuid)
    serializer = serializers.MockupTaskSerializer(task)
    return Response(serializer.data, status.HTTP_200_OK)

@api_view(['GET'])
def mockups_history(request):
    images = models.MockupImage.objects.all()
    serializer = serializers.MockupImageHistorySerializer(images, many=True)
    return Response(serializer.data, status.HTTP_200_OK)