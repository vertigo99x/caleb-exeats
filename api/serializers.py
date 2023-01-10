from rest_framework import serializers

from .models import Allusers, College, Student, Forms, Events, Descriptions, Hostels, Departments

from django.contrib.auth.models import User

class AllusersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Allusers
        fields = "__all__"
        

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"
        
        
class FormsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forms
        fields = "__all__"
        
class EventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = "__all__"
        

class DescriptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Descriptions
        fields = "__all__"
        
class CollegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = "__all__"
        
class DepartmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departments
        fields = "__all__"
        
class HostelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hostels
        fields = "__all__"
        





