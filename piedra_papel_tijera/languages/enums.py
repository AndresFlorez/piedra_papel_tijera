from django.utils.translation import ugettext as _
from collections import OrderedDict
from core.lib.fnutils import load_lib

global_enums = {}

global_enums['game_status_list'] = OrderedDict([
    ('', ''),
    ('0', _('Abierto')),
    ('1', _('Finalizado')),
])
