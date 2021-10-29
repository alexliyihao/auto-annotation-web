from django.shortcuts import render, get_object_or_404

from django.conf import settings
from .models import Image


def index(request):
    latest_image_list = Image.objects.order_by('-submission_date')
    context = {'latest_image_list': latest_image_list}
    return render(request, 'annotations/index.html', context)

def imageviews(request, image_id):
    image = get_object_or_404(Image, pk = image_id)
    return render(request, 'annotations/imageview.html', {'image':image, 'file_path':'/dzis/'})
