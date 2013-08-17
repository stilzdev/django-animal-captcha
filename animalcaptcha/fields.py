# -*- coding: utf-8 -*-

import datetime

from django.forms.widgets import TextInput, HiddenInput, MultiWidget
from django.forms.fields import CharField, MultiValueField
from django.forms import ValidationError
from django.utils.translation import ugettext_lazy

from animalcaptcha.models import AnimalCaptchaStore


class BaseAnimalCaptchaTextInput(MultiWidget):

    def __init__(self, attrs=None):
        widgets = (HiddenInput(attrs), TextInput(attrs), )
        super(BaseAnimalCaptchaTextInput, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return value.split(',')
        return [None, None]

    def render(self, name, value, attrs=None):
        return super(BaseAnimalCaptchaTextInput, self).render(name, self._value, attrs=attrs)


class AnimalCaptchaTextInput(BaseAnimalCaptchaTextInput):

    def __init__(self, attrs=None, **kwargs):
        self._args = kwargs
        self._args['output_format'] = self._args.get('output_format') or u'%(image)s %(hidden_field)s %(text_field)s'
        super(AnimalCaptchaTextInput, self).__init__(attrs)

    def format_output(self, rendered_widgets):
        hidden_field, text_field = rendered_widgets
        return self._args['output_format'] % {
            'image': '<img src="/captcha/image/{0}" /><br />'.format(self._key),
            'hidden_field': hidden_field,
            'text_field': text_field,
        }

    def render(self, name, value, attrs=None):
        key = AnimalCaptchaStore.generate_key()
        self._value, self._key, self.id_ = [key, u''], key, self.build_attrs(attrs).get('id', None)
        return super(AnimalCaptchaTextInput, self).render(name, self._value, attrs=attrs)


class AnimalCaptchaField(MultiValueField):

    def __init__(self, *args, **kwargs):
        fields = (CharField(show_hidden_initial=True), CharField(), )
        if 'error_messages' not in kwargs or 'invalid' not in kwargs.get('error_messages'):
            if 'error_messages' not in kwargs:
                kwargs['error_messages'] = {}
            kwargs['error_messages'].update({'invalid': ugettext_lazy('Invalid animal captcha!')})
        kwargs['widget'] = kwargs.pop('widget', AnimalCaptchaTextInput(output_format=kwargs.pop('output_format', None)))
        super(AnimalCaptchaField, self).__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        if data_list:
            return ','.join(data_list)
        return None

    def clean(self, value):
        super(AnimalCaptchaField, self).clean(value)
        response, value[1] = (value[1] or '').strip().lower(), ''
        AnimalCaptchaStore.remove_expired()
        try:
            AnimalCaptchaStore.objects.get(response=response, hashkey=value[0], expiration__gt=datetime.datetime.now()).delete()
        except AnimalCaptchaStore.DoesNotExist:
            raise ValidationError(getattr(self, 'error_messages', {}).get('invalid', ugettext_lazy('Invalid animal captcha!')))
        return value

