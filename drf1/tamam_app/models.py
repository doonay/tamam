from django.db import models
from django.contrib.postgres.fields import ArrayField

class Game(models.Model):
    id = models.AutoField(primary_key=True)
    product_id = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    platforms = ArrayField(models.CharField(max_length=255))
    base_price = models.IntegerField()
    discounted_price = models.IntegerField()
    discount = models.SmallIntegerField()
    img = models.CharField(max_length=255)
    last_modified = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title
    class Meta:
        abstract = True
            
class XboxGame(Game):
    class Meta:
        db_table = 'xbox_games'
'''
class PlayStationGame(Game):
    class Meta:
        db_table = 'playstation_games'
'''