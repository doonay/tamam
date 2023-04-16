from django.db import models
from django.urls import reverse

class EpicGame(models.Model):
    epic_id = models.CharField(unique=True, max_length=100)
    title = models.CharField(max_length=200)
    img = models.CharField(max_length=250)
    platforms = models.JSONField()
    #release = models.CharField(max_length=4)
    #release = models.DateTimeField()
    price_now = models.PositiveIntegerField()
    flag_is_discount = models.BooleanField()
    discount = models.PositiveIntegerField()
    price_past = models.PositiveIntegerField()
    timestrap = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('title', kwargs={'title': self.title})

class SteamGameModel(models.Model):
    steam_id = models.CharField(unique=True, max_length=100)
    title = models.CharField(max_length=200)
    game_link = models.CharField(max_length=250)
    img = models.CharField(max_length=250)
    platforms = models.JSONField()
    release_date = models.CharField(max_length=100)
    price_now = models.PositiveIntegerField()
    #---
    flag_is_discount = models.BooleanField()
    discount = models.PositiveIntegerField()
    price_past = models.PositiveIntegerField()
    #---
    flag_inner_prices = models.BooleanField()
    inner_prices = models.JSONField()
    #---
    timestrap = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

class PsDealsModel(models.Model):
    ps_id = models.CharField(max_length=250)
    title = models.CharField(max_length=100)
    platforms = models.JSONField()
    base_price = models.PositiveIntegerField()
    discounted_price = models.PositiveIntegerField()
    discount = models.PositiveIntegerField()
    is_free = models.BooleanField()
    is_exclusive = models.BooleanField()
    is_tied_to_subscription = models.BooleanField()
    img = models.CharField(max_length=250)
    #---
    timestrap = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class PsAllModel(models.Model):
    ps_id = models.CharField(max_length=250)
    title = models.CharField(max_length=100)
    platforms = models.JSONField()
    base_price = models.PositiveIntegerField()
    discounted_price = models.PositiveIntegerField()
    discount = models.PositiveIntegerField()
    is_free = models.BooleanField()
    is_exclusive = models.BooleanField()
    is_tied_to_subscription = models.BooleanField()
    img = models.CharField(max_length=250)
    #---
    timestrap = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class XboxGameModel(models.Model):
    xbox_id = models.CharField(max_length=250)
    title = models.CharField(max_length=100)
    img = models.CharField(max_length=250)
    platforms = models.JSONField()
    release_date = models.CharField(max_length=100)
    price_now = models.PositiveIntegerField()
    #---
    flag_is_discount = models.BooleanField()
    discount = models.PositiveIntegerField()
    price_past = models.PositiveIntegerField()

    def __str__(self):
        return self.title