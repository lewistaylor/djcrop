from PIL import Image
from django import forms
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import models
from django.db.models.fields.files import ImageField
from djcrop.widgets import CroppedImageWidget




class TempImage(models.Model):

    image = models.ImageField(upload_to='tmp')
