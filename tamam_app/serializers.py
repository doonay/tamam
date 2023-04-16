from .models import EpicGame

from rest_framework import serializers



        
class EpicGameSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EpicGame
        fields = ['epic_id', 'title', 'img', 'platforms', 'price_now', 'flag_is_discount', 'discount', 'price_past', 'timestrap']
