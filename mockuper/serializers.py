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
        data = [
            {
                "image_url": image.url,
                "created_at": image.created_at,
            } for image in images
        ]
        return data