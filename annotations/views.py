from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse,reverse_lazy
from django.conf import settings
from .models import Image, User
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegistrationForm
from datetime import datetime

class ImageListView(generic.ListView):
    '''
    The view for page image_list, for a brief skimming over the image list
    '''
    template_name = 'annotations/image_list.html'
    context_object_name = 'image_list'

    def get_queryset(self):
        """return the image-list """
        return Image.objects.order_by('-submission_date')
#def image_list(request):
    # get the image ordered by submission_date
#    image_list = Image.objects.order_by('-submission_date')
    # pass the imagelist to the file
#    context = {'image_list': image_list}
    # render the template
#    return render(request, 'annotations/image_list.html', context)

def image_views(request, image_id):
    '''
    The view for page image_view, for detailed annotations on a specific image
    '''
     try:
         # find the Image by image_id, or throw a 404 error
         image = Image.objects.get(pk = image_id)
         #please be noticed that file_path is only for debugging purpose, to be corrected
         return render(request, 'annotations/image_view.html', {'image':image, 'file_path':'/dzis/'})
     except(KeyError, Image.DoesNotExist):
         return HttpResponseRedirect(reverse('annotations:imagelist'))


#Deprecated for image_view settings
#class ImageViewsView(generic.DetailView):
#   model = Image
#   template_name = 'annotations/image_view.html'

class RegistrationView(generic.edit.CreateView):
    '''
    The view for page registration, for the registration of users
    '''
    template_name = 'annotations/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('annotations:regi-success')
    def form_valid(self, form):
        f = form.save(commit = False)
        f.register_date = datetime.now()
        f.save()
        return super().form_valid(form)

def registration_success_views(request):
    '''
    The view for page registration_success, for the success page of registration
    '''
    return render(request, "annotations/registration_success.html")
