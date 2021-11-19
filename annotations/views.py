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

from .models import Image, User, Annotation, Organization, ImageGroup
from .forms import (UserRegistrationForm, ImageUploadForm,\
                    UserLoginForm, AnnotationCreateform)

# Views
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

def extract_annotation(annotation):
    """
    extract the information from a Annotorious W3C Annotation,
    helper function in image view, the reason for duplicate saving
    is for faster rendering on image view while keep good management

    Input:
        Annotations: json instance, the Annotorious W3C Annotation

    Return:
        W3C_id: str, the W3C id generated by Annotorious
        annotation_class: str, the tag of annotation,
                          which is supposed to be empty or unique
        annotation_comment: str, the comment from the annotation,
                            which can be empty or there may be multiple comments
    """
    # This additional id is used for edit and deletions
    W3C_id = annotation['id']
    # The type of annotation try clause is to catch the scenario that the class is no declared
    try:
        # This will catch the first tag in the tagging list
        annotation_class = [info['value'] for info in annotation["body"] if info['purpose']=='tagging'][0]
    except IndexError:
        annotation_class = "Undecided"
    # The description
    # will catch all the comments, if there's no description, it will be ""
    description = "--".join([info['value'] for info in annotation["body"] if info['purpose'] =='commenting'])

    return W3C_id, annotation_class, description

def image_views(request, image_id):
    '''
    The view for page image_view, for detailed annotations on a specific image
    '''
    # if we are getting it via post, it's editing
    if request.method == 'POST':
        # get request from a ajax post request
        request_body = json.loads(request.body.decode("utf-8"))
        # get the action from the request
        action = request_body['action']
        if action == 'create_annotation':
            # init a form
            form = AnnotationCreateform(request.POST)
            # create a form instance
            f = form.save(commit = False)
            # Save the corresponding informations, this wordy one is for re-rendering
            f.contour = request_body['annotation']
            # Extract the W3C id, annotation class, and description for management
            f.W3C_id, f.annotation_class, f.description = extract_annotation(f.contour)
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
            delete_id = request_body['annotation']
            # find the instace to be deleted
            anno_tbd = Annotation.objects.get(W3C_id = delete_id)
            # delete the instance
            anno_tbd.delete()
            return HttpResponse(f'annotation {delete_id} deleted')
        elif action == 'update_annotation':
            # This update will update at the original instance,
            # in order to control the primary key scale
            # get the id need to be deleted
            update_id = request_body['previous']
            # find the instance to be updated
            anno_tbu = Annotation.objects.get(W3C_id = update_id)
            # Save the corresponding informations
            anno_tbu.contour = request_body['annotation']
            # Extract the W3C id, annotation class, and description for management
            anno_tbu.W3C_id, anno_tbu.annotation_class, anno_tbu.description = extract_annotation(anno_tbu.contour)
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
            # Filter returns a QuerySet object,
            # translate it into array with the Json format
            annotations = json.dumps({
                annotation_class:[
                    {
                    "w3c_id":i.W3C_id,
                    "contour":i.contour
                    }
                    for i
                    in Annotation.objects.filter(
                        image = image,
                        annotation_class = annotation_class
                        ).order_by("pk").iterator()
                    ] for annotation_class in settings.COLOR_MAP.keys()
                })

            # please be noticed that file_path is only for debugging purpose, to be corrected
            # This replace is to workaround the path requirement from models.filepathfield
            return render(
                        request,
                        'annotations/image_view.html',
                        {
                            'image_id':image.id,
                            'image_name': image.image_name,
                            'image_path':image.dzi_path.replace(settings.HOME_PATH,""),
                            'filepath':'/dzis/',
                            'annotations': annotations,
                            'COLOR_MAP': settings.COLOR_MAP
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
    success_url = reverse_lazy('annotations:registration-success')

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
            img = form.save(commit = False)
            # save the submission_date
            img.submission_date = timezone.now()
            # completely_annotated tag set to false
            img.completely_annotated = False
            # translated set to false
            img.translated = False
            # the user submit the image
            img.submit_user = User.objects.get(username=request.user.username)
            # save everything
            img.save()
            # This path is subject to change in actual deployment
            img.svs_path = f"{settings.HOME_PATH}/{settings.SVS_PATH}/{img.image_name}.svs"
            img.dzi_path = f"{settings.HOME_PATH}/{settings.DZI_PATH}/{img.image_name}.dzi"
            # openslide has poor support with python3.6+, run from external scripts
            dimensions = subprocess.check_output([
                                    "python3.5",
                                    f"{settings.HOME_PATH}/{settings.EXT_SCRIPT_PATH}/dimensions.py",
                                    f"{settings.HOME_PATH}/{settings.SVS_PATH}/{img.image_name}.svs"
                                    ])
            # interpret the result, the last character is newline character
            img.width, img.height = eval(dimensions.decode("utf-8")[:-1])
            img.save()
            # after the file is uploaded, run a translation procedure saving svs into dzis
            # It works internally as long as the server is not interrupted
            subprocess.Popen(['vips', 'dzsave', '{img.svs_path}', '{settings.HOME_PATH}/{settings.DZI_PATH}/{img.image_name};'])
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

def user_profile_view_self(request):
    """
    The view for user profile, for user's profile page
    """
    # get the user's instance from username(login system)
    user = User.objects.get(username=request.user.username)
    user_info = {
        "user": user
    }
    return render(request, "annotations/profile.html", user_info)

def user_profile_view_others(request, user_id):
    """
    The view for user profile, for other user's profile page
    """
    # get the user's instance from user id
    user = User.objects.get(id=user_id)
    user_info = {
        "user": user
    }
    return render(request, "annotations/profile.html", user_info)

def organization_profile_view_self(request):
    '''
    The view for page organization_view,
    for a brief skimming over the user's Organizaion
    '''
    # get the user's instance from username(login system)
    user = User.objects.get(username=request.user.username)
    # get the organization
    org = user.organizations
    # get the supervisor
    supervisor = org.supervisor
    # If the organization have no supervisor right now
    if supervisor != None:
        # search for all the non-supervisor member
        peoples = User.objects.filter(organizations = org).exclude(id = org.supervisor.id)
    else:
        # search for all the members
        peoples = User.objects.filter(organizations = org)
    return render(
        request,
        "annotations/organization_view.html",
        {
        "organization": org,
        "supervisor": supervisor,
        "member_list": peoples
        })

def organization_profile_view_others(request, organization_id):
    '''
    The view for page organization_view,
    for a brief skimming over the Organizaion <organization_id>
    '''
    # Get the organization by it's id
    org = Organization.objects.get(id=organization_id)
    # Get the supervisor
    supervisor = org.supervisor
    # If the organization have no supervisor right now
    if supervisor != None:
        # search for all the non-supervisor member
        peoples = User.objects.filter(organizations = org).exclude(id = org.supervisor.id)
    else:
        # search for all the members
        peoples = User.objects.filter(organizations = org)
    return render(
        request,
        "annotations/organization_view.html",
        {
        "organization": org,
        "supervisor": supervisor,
        "member_list": peoples
        })

def image_group_view(request, image_group_id):
    '''
    The view for page image_group_view,
    for a brief skimming over the image group <image_group_id>
    '''
    # Get the image group by image group
    image_group = ImageGroup.objects.get(id=image_group_id)
    # find the image in the image_group
    image_list = Image.objects.filter(group = image_group).order_by('-submission_date')
    return render(
        request,
        "annotations/image_group_view.html",
        {
        "image_group": image_group,
        "image_list": image_list
        })

def people_view(request):
    """
    The view for page people, viewing all the registered people.
    For we are running the system internally, this page is okay.
    """
    supervisor_ids = Organization.objects.filter(supervisor__isnull = False).values_list("supervisor", flat = True)
    supervisors = User.objects.filter(id__in = supervisor_ids)
    members = User.objects.all().exclude(id__in = supervisor_ids).order_by('organizations')
    return render(
        request,
        "annotations/people.html",
        {
        "supervisor_list": supervisors,
        "member_list": members
        })
