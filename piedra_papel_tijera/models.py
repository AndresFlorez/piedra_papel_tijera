from core.base.models import Base
from django.contrib.auth import get_user_model
from django.db import models
from django.forms.models import model_to_dict
from django.utils.translation import ugettext as _

User = get_user_model()

class Entity(Base):
    image_file = models.ImageField(upload_to='images', null=True, blank=True, verbose_name=_("Imagen"))

    def beat(self, other):
        if self.entity_strong.filter(entity_weak=other).exists(): return True
        elif self.entity_weak.filter(entity_strong=other).exists(): return False
        else: return None

    class Meta:
        db_table = 'entities'

class Rule(Base):
    entity_strong = models.ForeignKey(Entity, verbose_name=_("Entidad Fuerte"), blank=True, db_index=True, null=True, on_delete=models.CASCADE, related_name='entity_strong')
    entity_weak = models.ForeignKey(Entity, verbose_name=_("Entidad débil"), blank=True, db_index=True, null=True, on_delete=models.CASCADE, related_name='entity_weak')

    class Meta:
        db_table = 'rules'

class Game(Base):
    winner = models.ForeignKey(User, verbose_name=_("Ganador"), blank=True, db_index=True, null=True, on_delete=models.CASCADE, related_name='game_winner')
    loser = models.ForeignKey(User, verbose_name=_("Perdedor"), blank=True, db_index=True, null=True, on_delete=models.CASCADE, related_name='game_loser')
    player_1 = models.ForeignKey(User, verbose_name=_("Jugador 1"), blank=True, db_index=True, null=True, on_delete=models.CASCADE, related_name='player_one')
    player_2 = models.ForeignKey(User, verbose_name=_("Jugador 2"), blank=True, db_index=True, null=True, on_delete=models.CASCADE, related_name='player_two')
    entity_1 = models.ForeignKey(Entity, verbose_name=_("Entidad 1"), blank=True, db_index=True, null=True, on_delete=models.CASCADE, related_name='entity_one')
    entity_2 = models.ForeignKey(Entity, verbose_name=_("Entidad 2"), blank=True, db_index=True, null=True, on_delete=models.CASCADE, related_name='entity_two')
    status = models.BooleanField(blank=True, null=True, verbose_name=_("Estado"), default=False)

    class Meta:
        db_table = 'games'
