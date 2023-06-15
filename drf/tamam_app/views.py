from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Platform, Order, XboxGame, PlaystationGame, SteamGame
from .serializers import PlatformSerializer, OrderSerializer, XboxGameSerializer, PlaystationGameSerializer, SteamGameSerializer

class PlatformView(viewsets.ViewSet):
    
    def list(self, request):
        queryset = Platform.objects.all()
        serializer = PlatformSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Platform.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = PlatformSerializer(user)
        return Response(serializer.data)
    
class OrderView(viewsets.ViewSet):
    
    def list(self, request):
        queryset = Order.objects.all()
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Order.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = OrderSerializer(user)
        return Response(serializer.data)

class XboxGameView(viewsets.ViewSet):
    
    def list(self, request):
        queryset = XboxGame.objects.all()
        serializer = XboxGameSerializer(queryset, many=True)
        return Response(serializer.data)
    '''
    def retrieve(self, request, pk=None):
        queryset = XboxGame.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = XboxGameSerializer(user)
        return Response(serializer.data)
    '''
    def retrieve(self, request, pk=None):
        print(request)
        queryset = XboxGame.objects.all()
        
        if pk:
            queryset = queryset.filter(title__icontains=pk)
        
        serializer = XboxGameSerializer(queryset, many=True)
        return Response(serializer.data)

class PlaystationGameView(viewsets.ViewSet):
    def list(self, request):
        queryset = PlaystationGame.objects.all()
        serializer = PlaystationGameSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = PlayStationGame.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = PlayStationGameSerializer(user)
        return Response(serializer.data)

class SteamGameView(viewsets.ViewSet):
    
    def list(self, request):
        queryset = SteamGame.objects.all()
        serializer = SteamGameSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = SteamGame.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = SteamGameSerializer(user)
        return Response(serializer.data)

