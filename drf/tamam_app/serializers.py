from rest_framework import serializers
from .models import Platform, Order, XboxGame, PlaystationGame, SteamGame

class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        #fields = ('name',)
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    titles = serializers.ListField(child=serializers.CharField(max_length=255))
    platforms = serializers.ListField(child=serializers.CharField(max_length=255))
    class Meta:
        model = Order
        #fields = ('order_id', 'titles', 'platform', 'platforms', 'base_price', 'discounted_price', 'discount', 'last_modified')
        fields = '__all__'

class XboxGameSerializer(serializers.ModelSerializer):
    platforms = serializers.ListField(child=serializers.CharField(max_length=255))
    class Meta:
        model = XboxGame
        #fields = ('product_id', 'title', 'platform', 'platforms', 'base_price', 'discounted_price', 'discount', 'img', 'last_modified')
        fields = '__all__'

class PlaystationGameSerializer(serializers.ModelSerializer):
    platforms = serializers.ListField(child=serializers.CharField(max_length=255))
    class Meta:
        model = PlaystationGame
        #fields = ('product_id', 'title', 'platform', 'platforms', 'base_price', 'discounted_price', 'discount', 'img', 'last_modified')
        fields = '__all__'

class SteamGameSerializer(serializers.ModelSerializer):
    platforms = serializers.ListField(child=serializers.CharField(max_length=255))
    class Meta:
        model = SteamGame
        #fields = ('product_id', 'title', 'platform', 'platforms', 'base_price', 'discounted_price', 'discount', 'img', 'last_modified')
        fields = '__all__'
