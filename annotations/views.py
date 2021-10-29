from django.shortcuts import render, get_object_or_404

from django.conf import settings
from .models import Image


def index(request):
    # get the image ordered by submission_date
    latest_image_list = Image.objects.order_by('-submission_date')
    # pass the imagelist to the file
    context = {'latest_image_list': latest_image_list}
    # render the template
    return render(request, 'annotations/index.html', context)

def imageviews(request, image_id):
    # find the Image by image_id, or throw a 404 error
    image = get_object_or_404(Image, pk = image_id)
    #please be noticed that file_path is only for debugging purpose, to be corrected
    return render(request, 'annotations/imageview.html', {'image':image, 'file_path':'/dzis/'})
