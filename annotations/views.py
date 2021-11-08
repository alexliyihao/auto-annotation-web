from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse,reverse_lazy
from django.conf import settings
from .models import Image, User
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegistrationForm, ImageUploadForm, UserLoginForm, AnnotationCreateform
from datetime import datetime
import subprocess
from django.contrib.auth.views import LoginView, LogoutView

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
    # if we are getting it via post, it's editing
    if request.method == 'POST':
        form = AnnotationCreateform(request.POST)
        request_contour = request.POST.get('data', "error")
        print(f"contour get is {request_contour}")
        f = form.save(commit = False)
        f.contour = request_contour
        f.update_date = datetime.now()
        f.image = Image.objects.get(pk = image_id)
        f.annotator = User.objects.get(username=request.user.username)
        f.save()
        return JsonResponse(request_contour, safe = False) 
    # if we are getting it via get, it's reading
    else:
        try:
            # find the Image by image_id, or throw a 404 error
            image = Image.objects.get(pk = image_id)
            #please be noticed that file_path is only for debugging purpose, to be corrected
            # This replace is to workaround the path requirement from models.filepathfield
            return render(
                            request,
                            'annotations/image_view.html',
                            {
                                'image_id':image.id,
                                'image_name': image.image_name,
                                'image_path':image.dzi_path.replace("home/alexliyihao/",""),
                                'filepath':'/dzis/'
                            }
                        )
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
            f.translated = False
            f.save()
            # after the file is uploaded, run a translation procedure,
            # It works internally as long as the server is not interrupted
            # TBD: how to update the translated and the svs/dzi path?
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

def user_login_success_view(request):
    '''
    The view for page login_success, for user's login success page
    '''
    return render(request, "annotations/login_success.html")

class UserLogoutView(LogoutView):
    '''
    The view for page logout, for user's logout page
    '''
    template_name = "annotations/logout_success.html"
    next_page = reverse_lazy("annotations:logout-success")

def user_logout_success_view(request):
    '''
    The view for page logout_success, for user's login success page
    '''
    return render(request, "annotations/logout_success.html")

def contact_view(request):
    '''
    The view for page contact, for contact page
    '''
    return render(request, "annotations/contact.html")
