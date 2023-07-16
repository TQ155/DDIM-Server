from rest_framework import serializers

from .models import UploadedFiles
from .models import FileMetadata
from .models import CreateRule

class UploadedFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFiles
        fields = '__all__'

class FileMetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileMetadata
        fields = '__all__'

class CreateRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreateRule
        fields = '__all__'