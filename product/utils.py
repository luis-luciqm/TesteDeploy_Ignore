import random
import string
from django.utils.text import slugify
import requests
from io import BytesIO
from django.core.files.images import ImageFile
import urllib.request as urllib2

def random_string_generator(size = 10, chars = string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_slug_generator(instance, new_slug=None):
    """
    This is for a Django project and it assumes your instance 
    has a model with a slug field and a title character (char) field.
    """
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title) #dont modify this parameter.

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug = slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
                    slug = slug,
                    randstr = random_string_generator(size = 4)
                )
        return unique_slug_generator(instance, new_slug = new_slug)
    return slug


def download_image(url,file_name):
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"})
    binary_data = response.content
    temp_file = BytesIO()
    temp_file.write(binary_data)
    temp_file.seek(0)
    file_name = file_name + ".png"
    image = ImageFile(temp_file, name=file_name)
    return image