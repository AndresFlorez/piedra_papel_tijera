from django.contrib import admin

from .models import Game, Entity, Rule

class RuleAdmin(admin.ModelAdmin):
    model = Rule
    fields = ['entity_strong', 'name', 'entity_weak']
    list_display = ['entity_strong', 'name', 'entity_weak', 'creation_date']

admin.site.register(Game)
admin.site.register(Entity)
admin.site.register(Rule, RuleAdmin)
