from django import forms
from animalcaptcha.fields  import AnimalCaptchaField

class AnimalCaptchaForm(forms.Form):
    captcha = AnimalCaptchaField()
