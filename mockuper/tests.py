import tabnanny
from unittest.mock import patch, MagicMock
import os
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status

from mockuper import views, models


class ViewsAPITests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        # Ensure SAMPLE_IMAGES exists for tests that need it
        self.original_sample_images = os.environ.get('SAMPLE_IMAGES')

    def tearDown(self):
        # Restore env var
        if self.original_sample_images is None:
            os.environ.pop('SAMPLE_IMAGES', None)
        else:
            os.environ['SAMPLE_IMAGES'] = self.original_sample_images

    @patch('mockuper.views.AsyncResult')
    @patch('mockuper.views.group')
    @patch('mockuper.views.os.listdir')
    @patch('mockuper.views.tasks.create_mockup')
    def test_generate_mockup_shirt_success(
        self, 
        mock_create_mockup, 
        mock_listdir, 
        mock_group, 
        mock_async_result
        ):
        mock_listdir.return_value = ['img1.jpg', 'img2.jpg']

        # Mock create_mockup.s to return a simple signature placeholder
        mock_create_mockup.s = MagicMock(side_effect=lambda *args, **kwargs: ('sig', args, kwargs))

        # Mock group().delay() to return an object with id
        executed = MagicMock()
        executed.id = '0d93d887-7a9d-4619-ba6d-be9531f5c087'
        mock_group.return_value.delay.return_value = executed

        # Mock AsyncResult state
        mock_async_result.return_value.state = 'PENDING'

        request = self.factory.post(
            '/api/v1/mockups/generate/',
            {'text': 'Hello', 'font': 'arial'},
            format='json',
        )

        response = views.generate_mockup_shirt(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertIn('task_uuid', response.data, response.data)
        self.assertEqual(
            response.data['task_uuid'], '0d93d887-7a9d-4619-ba6d-be9531f5c087', response.data)
        self.assertIn('status', response.data, response.data)
        self.assertEqual(response.data['status'], 'PENDING', response.data)
        # Task should be persisted
        self.assertTrue(
            models.MockupTask.objects.filter(
                task_uuid='0d93d887-7a9d-4619-ba6d-be9531f5c087').exists(), response.data)

    def test_get_task_status_returns_200(self):
        # Create a task with a known UUID
        task_uuid = '0d93d887-7a9d-4619-ba6d-be9531f5c087'
        task = models.MockupTask.objects.create(task_uuid=task_uuid, status='PENDING')

        request = self.factory.get(f'/api/v1/tasks/{task.task_uuid}/')
        response = views.get_task_status(request, task_uuid=task.task_uuid)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('task_uuid'), task.task_uuid)
    
    def test_mockups_history_returns_200_and_list(self):
        request = self.factory.get('/api/v1/mockups/')
        response = views.mockups_history(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data['results'], list)