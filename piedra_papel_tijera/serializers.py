from django.contrib.auth import get_user_model
from rest_framework import serializers

from piedra_papel_tijera.models import Entity, Game

User = get_user_model()

class EntitySerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    name = serializers.ReadOnlyField()
    image_file = serializers.FileField()

    class Meta:
        model = Entity
        fields = ('id', 'name', 'image_file')

class GameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Game
        fields = ('id', 'winner', 'loser', 'player_1', 'player_2', 'entity_1', 'entity_2', 'status')

class UserSerializer(serializers.ModelSerializer):

    game_wins_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = '__all__'

    def get_game_wins_count(self, obj):
        return obj.game_winner.count()
