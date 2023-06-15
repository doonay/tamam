from rest_framework.routers import DefaultRouter
from .views import PlatformView, OrderView, XboxGameView, PlaystationGameView, SteamGameView

router = DefaultRouter()
router.register(r'platforms', PlatformView, basename='platforms')
router.register(r'orders', OrderView, basename='orders')
router.register(r'xbox_games', XboxGameView, basename='xbox_games')
router.register(r'playstation_games', PlaystationGameView, basename='playstation_games')
router.register(r'steam_games', SteamGameView, basename='steam_games')
urlpatterns = router.urls
