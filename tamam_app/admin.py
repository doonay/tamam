from django.contrib import admin
from .models import EpicGame
# Register your models here.

class EpicGameAdmin(admin.ModelAdmin):
    list_display = ['title']

admin.site.register(EpicGame,EpicGameAdmin)