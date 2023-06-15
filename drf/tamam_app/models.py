from django.db import models
from django.contrib.postgres.fields import ArrayField

class Platform(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        verbose_name = 'Platform'

class Game(models.Model):
    product_id = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    platform = models.ForeignKey('Platform', related_name='games', on_delete=models.CASCADE)
    #platforms = ArrayField(models.CharField(max_length=255))
    platforms = ArrayField(models.CharField(max_length=255), blank=True, null=True)
    base_price = models.IntegerField()
    discounted_price = models.IntegerField()
    discount = models.SmallIntegerField()
    img = models.CharField(max_length=255)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        managed = False
        abstract = True

class Order(models.Model):
    order_id = models.SlugField(max_length=255, blank=False, null=False, unique=True) # Это поле формируется отталкиваясь от даты и других данных заявки
    titles = ArrayField(models.CharField(max_length=255))
    platform = models.ForeignKey('Platform', related_name='orders', on_delete=models.CASCADE)
    platforms = ArrayField(models.CharField(max_length=255), blank=True, null=True)
    base_price = models.IntegerField()
    discounted_price = models.IntegerField()
    discount = models.SmallIntegerField()
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.order_id

    class Meta:
        verbose_name = 'Order'

class XboxGame(Game):
    platform = models.ForeignKey(Platform, related_name='xbox_games', on_delete=models.CASCADE)
    #platform = models.ForeignKey('Platform', related_name='xbox_games', default='playstation', on_delete=models.CASCADE, limit_choices_to={'xbox_games': 1})
    #platform = 'xbox'
    class Meta:
        #managed = False # с False джанга не редактирует таблицу
        db_table = 'xbox_games'
        verbose_name = 'Xbox game'

class PlaystationGame(Game):
    platform = models.ForeignKey(Platform, related_name='playstation_games', on_delete=models.CASCADE)
    class Meta:
        #managed = False # с False джанга не редактирует таблицу
        db_table = 'playstation_games'
        verbose_name = 'Playstation game'

class SteamGame(Game):
    #platform = models.ForeignKey(Platform, related_name='steam_games', on_delete=models.CASCADE)
    platform = models.ForeignKey('Platform', related_name='steam_games', on_delete=models.CASCADE)
    class Meta:
        #managed = False # с False джанга не редактирует таблицу
        db_table = 'steam_games'
        verbose_name = 'Steam game'