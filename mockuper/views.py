import os
from logging import getLogger
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from celery import group
from celery.result import AsyncResult
from mockuper import serializers, tasks, models

logger = getLogger(__name__)


@api_view(['POST'])
def generate_mockup_shirt(request):
    # Serializing the data
    serializer = serializers.MockupImageSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    text = serializer.validated_data['text']
    font = serializer.validated_data['font']

    try:
        # Creating the tasks
        files = os.listdir('mockuper/shirt_images')
        images_abs_path = [os.environ.get('SAMPLE_IMAGES') + file for file in files]

        # Saving the task to the database
        task = models.MockupTask.objects.create()

        # Creating the tasks signatures
        tasks_signatures = [tasks.create_mockup.s(text, path, font, task.id) for path in images_abs_path]
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
        logger.info(f"Mockup task group created: {executed_tasks.id}")
        return Response(data, status.HTTP_201_CREATED)
    except Exception as e:
        logger.error(f"Error creating mockup task: {str(e)}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_task_status(request, task_uuid):
    task = get_object_or_404(models.MockupTask, task_uuid=task_uuid)
    serializer = serializers.MockupTaskSerializer(task, context={'request': request})
    return Response(serializer.data, status.HTTP_200_OK)

@api_view(['GET'])
def mockups_history(request):
    images = models.MockupImage.objects.all().order_by('-created_at')
    paginator = PageNumberPagination()
    # Allow clients to control page size with a sensible default
    page_size = request.query_params.get('page_size')
    if page_size is not None:
        try:
            paginator.page_size = max(1, min(int(page_size), 100))
        except (TypeError, ValueError):
            paginator.page_size = 10
    else:
        paginator.page_size = 10

    page = paginator.paginate_queryset(images, request)
    serializer = serializers.MockupImageHistorySerializer(page, many=True)
    return paginator.get_paginated_response(serializer.data)