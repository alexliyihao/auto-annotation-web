from django.db import models
from django.contrib.auth.models import User as auth_user

class User(auth_user):
    """
    individual user entity, it inherits the username,
    password, first name, last name, and email from django.contrib.auth.models.User
    """
    # UNI
    UNI = models.CharField(max_length = 8, unique=True)
    # The date user registered
    register_date = models.DateTimeField('date of registration', blank = True)
    # The organization this user belongs to
    organizations = models.ForeignKey('Organization', on_delete=models.PROTECT,null = True, blank = True)
    def __str__(self):
      return f"{self.UNI} - {self.first_name} {self.last_name}"

class Organization(models.Model):
    """
    Organization identity
    """
    # The name of the organization
    organization_name = models.CharField(max_length = 40, unique=True)
    # The supervisor of the organization
    supervisor = models.ForeignKey(User, on_delete=models.SET_NULL, null = True, blank = True)

    def __str__(self):
      return self.organization_name

class ImageGroup(models.Model):
    """
    The group of whole slide image group, for management purpose
    """
    # The name of this group
    group_name = models.CharField(max_length = 200, unique=True)
    # The description to this group
    group_description = models.TextField()

    def __str__(self):
      return self.group_name

class Image(models.Model):
    """
    The whole slide image identity
    """
    # Name of the image
    image_name = models.CharField(max_length = 200, unique=True)
    # The date submitted
    submission_date = models.DateTimeField('date of submission')
    # The upload specific field for uploading
    image_upload = models.FileField(upload_to = 'svss/')
    # The upload specific field as traslating indicator
    translated = models.BooleanField(default= 'False')
    # The path of Aperio SVS file(original file)
    svs_path = models.FilePathField(path = "/home/alexliyihao/svss", match = ".*\.svs")
    # The path of Deep Zoom Image(dzi) file generated from svs file
    dzi_path = models.FilePathField(path = "/home/alexliyihao/dzis", match = ".*\.dzi")
    # The height of the SVS file
    height = models.PositiveIntegerField()
    # The width of the SVS file
    width = models.PositiveIntegerField()
    # The description to the individual image
    image_description = models.TextField()
    # The boolean variable indicate if the image is fully annotated
    completely_annotated = models.BooleanField(default = 'False')
    # The group this image belongs to
    group = models.ForeignKey(ImageGroup, on_delete=models.SET_NULL, blank = True, null = True)
    # The user who submit this image
    submit_user = models.ForeignKey(User, on_delete=models.PROTECT, blank = True, null = True)

    def __str__(self):
       return self.image_name

class Annotation(models.Model):
    """
    Each individual annotation entity
    """
    # The contour of the annotation
    contour = models.JSONField()
    # The date this annotation is updated
    update_date = models.DateTimeField('date submit this annotation')
    # The image it belongs to
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    # The user who submitted this annotation
    annotator = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
       return f"{self.image}_{self.annotator}_{self.update_date}"
