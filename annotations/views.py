from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse,reverse_lazy
from django.conf import settings
from .models import Image, User
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegistrationForm, ImageUploadForm, UserLoginForm
from datetime import datetime
import subprocess
from django.contrib.auth import LoginView
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
        # This replace is to workaround the path requirement from models.filepathfield
        return render(request, 'annotations/image_view.html', {'image_path':image.dzi_path.replace("home/alexliyihao/",""), 'filepath':'/dzis/'})
    except(KeyError, Image.DoesNotExist):
        return HttpResponseRedirect(reverse('annotations:image-list'))


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

def handle_uploaded_file(file, des_path):
    """
    helper function of image_uploading_views dealing with large svs files,
    left here for checking
    """
    with open(def_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def image_upload_views(request):
    '''
    The view for page image_upload, for upload a new file
    '''
    if request.method == "POST":
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            f = form.save(commit = False)
            f.submission_date = datetime.now()
            f.svs_path = f"svss/{f.image_name}.svs"
            f.dzi_path = f"dzis/{f.image_name}.dzi"
            # openslide has poor support with python3.5+, so run it from external scripts
            dimensions = subprocess.check_output([
                                    "python3.5",
                                    "../ext_script/dimensions.py",
                                    "../svss/test.svs"
                                    ])
            # interpret the result, the last character is newline character
            f.width, f.height = eval(dimensions.decode("utf-8")[:-1])
            f.completely_annotated = False
	    # TBD: See the line below
            f.translated = True
            f.save()
            # after the file is uploaded, run a translation procedure
            # TBD: can we run it internally rather than on the page? It takes too long
            subprocess.Popen(['vips', 'dzsave', f"../{f.svs_path}",f'../dzis/{f.image_name}'])
            return HttpResponseRedirect(reverse_lazy('annotations:image-upload-success'))
        else:
            print(form.errors)
    else:
        form = ImageUploadForm()
    return render(request, 'annotations/image_upload.html', {'form': form})

def image_upload_success_views(request):
    '''
    The view for page image_upload_success, for the success page of image uploading process
    '''
    return render(request, "annotations/image_upload_success.html")

class UserLoginView(LoginView):
    '''
    The view for page login, for the user's login page
    '''
    template_name = "annotations/login.html"
    authentication_form = UserLoginForm
    redirect_authenticated_user = False
