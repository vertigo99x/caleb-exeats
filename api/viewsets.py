from tkinter.tix import Form
from rest_framework import viewsets
from .models import Allusers, Student, Forms, Events
from .serializers import AllusersSerializer,StudentSerializer, EventsSerializer, FormsSerializer


class FormsViewset(viewsets.ModelViewSet):
    queryset = Forms.objects.all()
    serializer_class = FormsSerializer
