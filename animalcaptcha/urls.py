try:
    from django.conf.urls import patterns, url
except ImportError:
    from django.conf.urls.defaults import patterns, url

urlpatterns = patterns(
    'animalcaptcha.views',
    url(r'image/(?P<key>\w+)$', 'animal_captcha_image', name='captcha-image'),
)

