import json

from django.contrib.auth import get_user_model
from django.db.models import Count, F, Q
from rest_framework import static, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import (LimitOffsetPagination,
                                       PageNumberPagination)
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Entity, Game, Rule
from .serializers import EntitySerializer, GameSerializer, UserSerializer

User = get_user_model()

class EntityAPI(viewsets.ModelViewSet):
    serializer_class = EntitySerializer
    queryset = Entity.objects.all()
    pagination_class = PageNumberPagination

    @action(methods=['POST'], detail=False, name="challenge")
    def challenge(self, request):
        try:
            game_id = request.POST.get('id', None)
            entity_1 = request.POST.get('entity_1', None)
            entity_2 = request.POST.get('entity_2', None)
            player_1 = request.POST.get('player_1', None)
            player_2 = request.POST.get('player_2', None)
            game = Game.objects.filter(id=game_id).first()

            if not game:
                q1 = Q(player_1_id=player_1) & Q(player_2_id=player_2)
                q2 = Q(player_2_id=player_1) & Q(player_1_id=player_2)
                game = Game.objects.filter(q1 | q2, status=False).first()
                if game:
                    entity_2 = entity_1

            if not game:
                game = Game()
                game.player_1_id = player_1
                game.entity_1_id = entity_1
                game.player_2_id  = player_2
            else:
                entity_2 = Entity.objects.get(id=entity_2)
                result = game.entity_1.beat(entity_2)
                game.entity_2 = entity_2
                if result is True:
                    game.winner_id = game.player_1
                    game.loser_id = game.player_2
                elif result is False:
                    game.winner_id = game.player_2
                    game.loser_id = game.player_1
                else:  # EMPATE
                    pass
                game.status = True
            game.save()
            serializer = GameSerializer(game)
            return Response(serializer.data)
        except Exception as e:
            raise
            return Response(status=status.HTTP_404_NOT_FOUND)
    

    @action(methods=['POST'], detail=False, name="get_match")
    def get_match(self, request):
        try:
            user_id = request.POST.get('user_id')
            q1 = Q(player_1_id=request.user.id) & Q(player_2_id=user_id)
            q2 = Q(player_2_id=request.user.id) & Q(player_1_id=user_id)
            game = Game.objects.get(q1 | q2, status=False)

            serializer = GameSerializer(game)
            return Response(serializer.data)
        except Exception as e:
            return Response(status=status.HTTP_404_NOT_FOUND)


class RankingPagination(PageNumberPagination):
    page_size = 5

class UserAPI(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all().annotate(count=Count('game_winner__id')).order_by('-count')
    pagination_class = RankingPagination
