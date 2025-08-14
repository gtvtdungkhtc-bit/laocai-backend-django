from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Road, Asset, Project, UserProfile

class RoadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Road
        fields = '__all__'

class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source='profile.role', read_only=True)
    unit = serializers.CharField(source='profile.unit', read_only=True)

    class Meta:
        model = User
        fields = ['id','username','first_name','last_name','email','role','unit']
