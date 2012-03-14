from django.db import models
from djcrop.fields import CroppedImageField

# Create your models here.


class MyTest(models.Model):
    
    image = CroppedImageField(upload_to='test')