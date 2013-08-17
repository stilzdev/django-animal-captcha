# -*- coding: utf-8 -*-

import os

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext

from animalcaptcha.conf import settings
from animalcaptcha.models import AnimalCaptchaStore

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    import Image, ImageDraw, ImageFont

from StringIO import StringIO
import random

def create_filled_image(size):
    image = Image.new('RGB', size)
    for x in range(size[0]):
        for y in range(size[1]):
            image.putpixel((x, y), (122, 122, 122))
    return image

def paste_images(destination, first_image, second_image, margin):
    destination.paste(
        first_image,
        (margin, margin, first_image.size[0] + margin, first_image.size[1] + margin)
    )
    destination.paste(
        second_image,
        (
            first_image.size[0] + 2 * margin,
            margin,
            first_image.size[0] + second_image.size[0] + 2 * margin,
            second_image.size[1] + margin
        )
    )

def add_text_at_bottom(image, text, margin):
    font = ImageFont.truetype(os.path.join(os.path.dirname(__file__), 'fonts', 'Quivira.ttf'), 24)# '/usr/share/fonts/truetype/ttf-dejavu/DejaVuSans-Bold.ttf', 24)
    draw = ImageDraw.Draw(image)
    textSize = draw.textsize(text, font=font)
    draw.text((image.size[0] / 2 - textSize[0] / 2, image.size[1] - 24 - margin), text, font=font)

def pick_random_image_from_directory(directory):
    all_files = [
        f for f in os.listdir(os.path.join(settings.ANIMAL_CAPTCHA_BASE_IMAGES_DIR, directory))
        if f.endswith('.jpg')
    ]
    image = Image.open(
        os.path.join(settings.ANIMAL_CAPTCHA_BASE_IMAGES_DIR, directory, random.choice(all_files))
    )
    return image.resize((settings.ANIMAL_CAPTCHA_SIZE[0] / 2 , settings.ANIMAL_CAPTCHA_SIZE[1] / 2))


def pick_image_directories_for_challenge(challenge):
    challenge_directory_ = settings.ANIMAL_CAPTCHA_IMAGE_DIRS[challenge]
    other_directories = settings.ANIMAL_CAPTCHA_IMAGE_DIRS.values()
    other_directories.remove(challenge_directory_)
    additional_directory_ = random.choice(other_directories)
    challenge_side = ['left', 'right'][random.random() > 0.5]
    if 'left' == challenge_side:
        challenge_directory = challenge_directory_
        additional_directory = additional_directory_
    else:
        challenge_directory = additional_directory_
        additional_directory = challenge_directory_
    return challenge_directory, additional_directory, challenge_side

def calculate_image_size(left_image, right_image, margin):
    return (
        left_image.size[0] + right_image.size[0] + 3 * margin,
        max(left_image.size[1], right_image.size[1]) + 3 * margin + 24
    )

def convert_image_to_http_response(image):
    out = StringIO()
    image.save(out, "PNG")
    out.seek(0)
    response = HttpResponse(content_type='image/png')
    response.write(out.read())
    response['Content-length'] = out.tell()
    return response

def animal_captcha_image(request, key):
    animal_captcha_size = settings.ANIMAL_CAPTCHA_SIZE
    store = get_object_or_404(AnimalCaptchaStore, hashkey=key)

    margin = 10

    first_directory, second_directory, challenge_side = pick_image_directories_for_challenge(store.challenge)
    left_image = pick_random_image_from_directory(first_directory)
    right_image = pick_random_image_from_directory(second_directory)

    if 'left' == challenge_side:
        text = ugettext('What animal do you see on the left side?')
    else:
        text = ugettext('What animal do you see on the right side?')

    size = calculate_image_size(left_image, right_image, margin)
    image = create_filled_image(size)
    paste_images(image, left_image, right_image, margin)
    add_text_at_bottom(image, text, margin)
    image = image.resize(animal_captcha_size)

    return convert_image_to_http_response(image)

