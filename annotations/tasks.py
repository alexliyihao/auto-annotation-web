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

@shared_task
def get_size(img_id, svs_path):
    """
    run a openslide script {settings.HOME_PATH}/{settings.EXT_SCRIPT_PATH}/dimensions.py in python 3.5
    the addtional arg is the path of svs file {settings.HOME_PATH}/{settings.SVS_PATH}/{image_name}.svs
    then update the image size to the image with img_id
    """
    # openslide has poor support with python3.6+, run from external scripts
    dimensions = subprocess.check_output([
                            "python3.5",
                            f"{settings.HOME_PATH}/{settings.EXT_SCRIPT_PATH}/dimensions.py",
                            svs_path
                            ])
    # for we cannot directly use the object instance, re-access the Image object
    image_tbu = Image.objects.get(id = img_id)
    # interpret the result, the last character is newline character
    image_tbu.width, image_tbu.height = eval(dimensions.decode("utf-8")[:-1])
    # save the updates
    image_tbu.save()
