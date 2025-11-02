import os
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from celery import group
from mockuper import serializers
from mockuper import tasks


@api_view(['POST'])
def generate_mockup_shirt(request):
    serializer = serializers.MockupImageSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    text = request.data['text']
    files = os.listdir('mockuper/shirt_images')
    images_abs_path = [os.environ.get('SAMPLE_IMAGES') + file for file in files]
    tasks_signatures = [tasks.create_mockup.s(text, path) for path in images_abs_path]
    multiple_mockup_tasks = group(tasks_signatures)
    executed_tasks = multiple_mockup_tasks.delay()
    # mockup_image = serializer.save(url=task)
    data = {
        'task_id': executed_tasks.id,
        'status': 'PENDING',
        'message': 'ساخت تصویر آغاز شد'
    }
    return Response(data, status.HTTP_201_CREATED)