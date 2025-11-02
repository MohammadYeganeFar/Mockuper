from rest_framework import serializers
from mockuper import models


class MockupImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.MockupImage
        fields = ['text']


