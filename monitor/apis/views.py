from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets
from .serializers import LogsSerializer
from .models import Historicallogs
from core.models import Website

class LogsViewSet(viewsets.ModelViewSet):
    queryset = Historicallogs.objects.all()
    serializer_class = LogsSerializer