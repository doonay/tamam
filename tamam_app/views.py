from django.shortcuts import render, get_object_or_404
from .models import EpicGame
from rest_framework import viewsets
from .serializers import EpicGameSerializer
from django.http import JsonResponse, HttpResponse

def index(request):
    #brand=CarBrand.objects.all()
    brand=[{
        'value': "jquery",
        'label': "jQuery",
        'desc': "the write less, do more, JavaScript library",
        'icon': "jquery_32x32.png"
      },
      {
        'value': "jquery-ui",
        'label': "jQuery UI",
        'desc': "the official user interface library for jQuery",
        'icon': "jqueryui_32x32.png"
      },
      {
        'value': "sizzlejs",
        'label': "Sizzle JS",
        'desc': "a pure-JavaScript CSS selector engine",
        'icon': "sizzlejs_32x32.png"
      }]
    return render(request,'index.html',{'brand':brand})

def payment(request, title):
    print(title)
    return HttpResponse(f'Отображение игры с айди = {title}')

def show_game(request, title):
    #print(title)
    obj = get_object_or_404(EpicGame, title=title)
    context = {
      'game_data':{
        'title' : obj.title,
        'epic_id' : obj.epic_id,
        'title' : obj.title,
        'img' : obj.img,
        'platforms' : obj.platforms,
        'price_now' : obj.price_now,
        'flag_is_discount' : obj.flag_is_discount,
        'discount' : obj.discount,
        'price_past' : obj.price_past,
        'timestrap' : obj.timestrap,
      }
    }
    #print(context)
    return render(request, 'payment.html', context=context)



class EpicGameViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = EpicGame.objects.all()
    serializer_class = EpicGameSerializer

def get_games(request):
  search = request.GET.get('search')
  payload = []
  if search:
    objs = EpicGame.objects.filter(title__startswith = search)

    for obj in objs:
      payload.append({
        'epic_id' : obj.epic_id,
        'title' : obj.title,
        'img' : obj.img,
        'platforms' : obj.platforms,
        'price_now' : obj.price_now,
        'flag_is_discount' : obj.flag_is_discount,
        'discount' : obj.discount,
        'price_past' : obj.price_past,
        'timestrap' : obj.timestrap,
      })

  return JsonResponse({
    'status' : True,
    'payload' : payload
  })  

