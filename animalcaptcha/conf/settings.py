import os

from django.conf import settings
from django.utils.translation import ugettext

ANIMAL_CAPTCHA_BASE_IMAGES_DIR = getattr(
    settings,
    'ANIMAL_CAPTCHA_BASE_IMAGES_DIR',
    os.path.join(os.path.dirname(__file__), '..', '..', 'animals')
)
ANIMAL_CAPTCHA_IMAGE_DIRS = getattr(
    settings,
    'ANIMAL_CAPTCHA_IMAGE_DIRS',
    {
        ugettext('cat'): 'cats',
        ugettext('dog'): 'dogs',
        ugettext('horse'): 'horses',
        ugettext('frog'): 'frogs',
        ugettext('lion'): 'lions',
        ugettext('tiger'): 'tigers',
        ugettext('fish'): 'fishes',
        ugettext('snake'): 'snakes',
    }
)
ANIMAL_CAPTCHA_SIZE = getattr(settings, 'ANIMAL_CAPTCHA_SIZE', (800, 400))

