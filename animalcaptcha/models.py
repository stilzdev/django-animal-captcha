from django.db import models

from animalcaptcha.conf import settings

import datetime
import random
import time
import unicodedata
import hashlib

def get_challenge():
    options = settings.ANIMAL_CAPTCHA_IMAGE_DIRS.keys()
    ret = random.choice(options)
    return ret, ret

MAX_RANDOM_KEY = 2 << 63

class AnimalCaptchaStore(models.Model):

    challenge = models.CharField(blank=False, max_length=32)
    response = models.CharField(blank=False, max_length=32)
    hashkey = models.CharField(blank=False, max_length=40, unique=True)
    expiration = models.DateTimeField(blank=False)

    def save(self, *args, **kwargs):
        self.response = self.response.lower()
        if not self.expiration:
            self.expiration = datetime.datetime.now() + datetime.timedelta(minutes=10)
        if not self.hashkey:
            import re
            key_ = unicodedata.normalize('NFKD', unicode(random.randrange(0, MAX_RANDOM_KEY)) + unicode(time.time()) + re.sub('[^a-z0-9]', '_', self.challenge.lower()))
            self.hashkey = hashlib.sha1(key_).hexdigest()
            del key_
        super(AnimalCaptchaStore, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.challenge

    @classmethod
    def generate_key(cls):
        challenge, response = get_challenge()
        store = cls.objects.create(challenge=unicode(challenge), response=unicode(response))
        return store.hashkey

    def remove_expired(cls):
        cls.objects.filter(expiration__lte=datetime.datetime.now()).delete()
    remove_expired = classmethod(remove_expired)

