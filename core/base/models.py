from django.db import models
from django.utils.translation import ugettext as _

# Base class Definition
class Base(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Fecha de creación'))
    last_update = models.DateTimeField(auto_now=True, verbose_name=_('Última modificación'))
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Nombre"))

    def __str__(self):
        if self.name:
            return str(self.name)
        else:
            return ''
    
    class Meta:
        abstract = True