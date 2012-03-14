'''
Created on 8 Mar 2012

@author: captain
'''
from django import forms
from djcrop.fields import CroppedImageFormField
from djcrop.models import TempImage


class TempImageForm(forms.ModelForm):

    image = CroppedImageFormField(required=False)

    class Meta:
        model = TempImage