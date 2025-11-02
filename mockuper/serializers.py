from rest_framework import serializers
from mockuper import models


class MockupImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.MockupImage
        fields = ['text']


class MockupTaskSerializer(serializers.ModelSerializer):
    results = serializers.SerializerMethodField()

    class Meta:
        model = models.MockupTask
        fields = ['task_uuid', 'status', 'results']

    def get_results(self, obj):
        images = obj.images.all()
        request = self.context.get('request')
        base_url = request.build_absolute_uri('/')[:-1] if request else 'http://127.0.0.1:8000'
        
        data = [
            {
                "image_url": f"{base_url}/{image.url}" if not image.url.startswith('http') else image.url,
                "created_at": image.created_at,
            } for image in images
        ]
        return data


class MockupImageHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MockupImage
        fields = ['id', 'text', 'url', 'created_at']