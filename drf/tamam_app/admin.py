from django.contrib import admin
from .models import Platform, Order, XboxGame, PlaystationGame, SteamGame


#class XboxGameAdmin(admin.ModelAdmin): # переопределяем поле класса в ридонли, что бы в админке было не поменять
#    readonly_fields = ('platform',)

class SteamGameAdmin(admin.ModelAdmin):
    readonly_fields = ('platform',)

class PlaystationGameAdmin(admin.ModelAdmin):
    readonly_fields = ('platform',)

admin.site.register(Platform)
admin.site.register(Order)
#admin.site.register(XboxGame, XboxGameAdmin)
admin.site.register(XboxGame)
admin.site.register(SteamGame, SteamGameAdmin)
admin.site.register(PlaystationGame, PlaystationGameAdmin)
