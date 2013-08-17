from django import forms
from animalcaptcha.fields import AnimalCaptchaField
from django.template import RequestContext
from django.http import HttpResponseRedirect
from forms import AnimalCaptchaForm
from django.shortcuts import render_to_response


def demo(request):
    if request.POST:
        form = AnimalCaptchaForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect(request.path + '?ok')
    else:
        form = AnimalCaptchaForm()

    return render_to_response('index.html', dict(
        form=form
    ) , context_instance=RequestContext(request))
