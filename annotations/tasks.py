from celery import shared_task
from django.conf import settings
from .models import Image
import subprocess

@shared_task
def translate(img_id, svs_path, image_name):
    """
    run libvips' dzsave command translating the svs files in <svs_path>
    to dzi file in settings.DZI_PATH
    Django model is not serializable so have the strings and ids passed in seperately
    args:
	img_id: the id(pk) of the image
        svs_path: string, the svs_path of the image
        image_name: string, the image's name for generating the dzi_path 
    """
    # run libvips
    process = subprocess.check_call(['vips', 'dzsave', f'{svs_path}', f'{settings.HOME_PATH}/{settings.DZI_PATH}/{image_name}'])
    # for we cannot directly use the object instance, re-access the Image object
    image_tbu = Image.objects.get(id = img_id)
    # updated the "translated" tag
    image_tbu.translated = True
    # save the updates
    image_tbu.save()
    
