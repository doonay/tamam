from rest_framework.response import Response
from rest_framework.views import APIView
from .models import XboxGame
from .serializers import XboxGameSerializer

class GameView(APIView):
    def get(self, request):
        xbox_games = XboxGame.objects.all()
        # the many param informs the serializer that it will be serializing more than a single game.
        serializer = XboxGameSerializer(xbox_games, many=True)
        return Response({"xbox_games": serializer.data})
