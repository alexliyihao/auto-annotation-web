from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.urls import reverse,reverse_lazy
from django.conf import settings
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.views import generic

import pytz
import subprocess
import json

from .models import Image, User, Annotation
from .forms import UserRegistrationForm, ImageUploadForm, UserLoginForm, AnnotationCreateform

class ImageListView(generic.ListView):
    '''
    The view for page image_list, for a brief skimming over the image list
    '''
    template_name = 'annotations/image_list.html'
    context_object_name = 'image_list'

    def get_queryset(self):
        """
        helper function returning the image-list
        """
        return Image.objects.order_by('-submission_date')

def image_views(request, image_id):
    '''
    The view for page image_view, for detailed annotations on a specific image
    '''
    # if we are getting it via post, it's editing
    if request.method == 'POST':
        # get request from a ajax post request
        request = json.loads(request.body.decode("utf-8"))
        # get the action from the request
        action = request['action']
        if action == 'create_annotation':
            # init a form
            form = AnnotationCreateform(request.POST)
            # create a form instance
            f = form.save(commit = False)
            # Save the corresponding informations
            f.contour = request['annotation']
            # This additional id is used for edit and deletions
            f.W3C_id = f.contour['id']
            # The time is current time
            f.update_date = timezone.now()
            # The image belonging is grabbed from the image_id
            f.image = Image.objects.get(pk = image_id)
            # The user is the user submitting the request
            f.annotator = User.objects.get(username=request.user.username)
            # saving the files
            f.save()
            return HttpResponse(f'annotation {f.W3C_id} saved')
        elif action == 'delete_annotation':
            # get the id need to be deleted
            delete_id = request['annotation']
            # find the instace to be deleted
            anno_tbd = Annotation.objects.get(W3C_id = delete_id)
            # delete the instance
            anno_tbd.delete()
            return HttpResponse(f'annotation {delete_id} deleted')
        elif action == 'update_annotation':
            # This update will update at the original instance,
            # in order to control the primary key scale
            # get the id need to be deleted
            update_id = request['previous']
            # find the instance to be updated
            anno_tbu = Annotation.objects.get(W3C_id = update_id)
            # Save the corresponding informations
            anno_tbu.contour = request['annotation']
            # This additional id is used for edit and deletions
            anno_tbu.W3C_id = anno_tbu.contour['id']
            # The time is current time
            anno_tbu.update_date = timezone.now()
            # save the instance
            anno_tbu.save()
            return HttpResponse(f'annotation {anno_tbu.W3C_id} updated')
    # if we are getting it via get, it's reading
    else:
        try:
            # find the Image by image_id
            image = Image.objects.get(pk = image_id)
            # Scan the annotation set for the annotation on this image
            # Filter returns a QuerySet object, translate it into array with the Json format
            annotation_set = json.dumps([i.contour for i in Annotation.objects.filter(image = image).iterator()])
            # please be noticed that file_path is only for debugging purpose, to be corrected
            # This replace is to workaround the path requirement from models.filepathfield
            return render(
                        request,
                        'annotations/image_view.html',
                        {
                            'image_id':image.id,
                            'image_name': image.image_name,
                            'image_path':image.dzi_path.replace("home/alexliyihao/",""),
                            'filepath':'/dzis/',
                            'annotation_set': annotation_set
                        }
                    )
        except(KeyError, Image.DoesNotExist):
            return HttpResponseRedirect(reverse('annotations:image-list'))

class RegistrationView(generic.edit.CreateView):
    '''
    The view for page registration, for the registration of users
    '''
    template_name = 'annotations/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('annotations:regi-success')

    def form_valid(self, form):
        '''
        helper function adding the register_date
        '''
        f = form.save(commit = False)
        f.register_date = timezone.now()
        f.password = make_password(f.password)
        f.save()
        return super().form_valid(form)

def registration_success_views(request):
    '''
    The view for page registration_success, for the success page of registration
    '''
    return render(request, "annotations/registration_success.html")

#def handle_uploaded_file(file, des_path):
#    """
#    helper function of image_uploading_views dealing with large svs files,
#    left here for checking, not using yet
#    """
#    with open(def_path, 'wb+') as destination:
#        for chunk in f.chunks():
#            destination.write(chunk)

def image_upload_views(request):
    '''
    The view for page image_upload, for upload a new file
    '''
    # A post request is uploading a image
    if request.method == "POST":
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Init a form
            f = form.save(commit = False)
            # save the submission_date
            f.submission_date = timezone.now()
            # completely_annotated tag set to false
            f.completely_annotated = False
            # translated set to false
            f.translated = False
            # the user submit the image
            f.submit_user = User.objects.get(username=request.user.username)
            # save everything
            f.save()
            # This path is subject to change in actual deployment
            f.svs_path = f"/home/alexliyihao/svss/{f.image_name}.svs"
            f.dzi_path = f"/home/alexliyihao/dzis/{f.image_name}.dzi"
            # openslide has poor support with python3.6+, run from external scripts
            dimensions = subprocess.check_output([
                                    "python3.5",
                                    "../ext_script/dimensions.py",
                                    f"../svss/{f.image_name}.svs"
                                    ])
            # interpret the result, the last character is newline character
            f.width, f.height = eval(dimensions.decode("utf-8")[:-1])
            f.save()
            # after the file is uploaded, run a translation procedure saving svs into dzis
            # It works internally as long as the server is not interrupted
            subprocess.Popen(['vips', 'dzsave', f"{f.svs_path}",f'/home/alexliyihao/dzis/{f.image_name}'])
            # TBD: how to update the translated tag later?
            return HttpResponseRedirect(reverse_lazy('annotations:image-upload-success'))
        else:
            print(form.errors)
    # when using a get method, render the page
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

def user_profile_view(request):
    """
    The view for user profile, for user's profile page
    """
    # get the user's instance from username(login system)
    user = User.objects.get(username=request.user.username)
    user_info = {
      "username": user.username,
      "firstname": user.first_name,
      "lastname": user.last_name,
      "UNI": user.UNI,
      "email": user.email,
      "organization": user.organizations,
      "register_date": user.register_date,
    }
    return render(request, "annotations/profile.html", user_info)
