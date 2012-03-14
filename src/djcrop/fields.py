from PIL import Image
from django import forms
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models.fields.files import ImageField
from djcrop.models import TempImage
from djcrop.widgets import CroppedImageWidget


        
        

class CroppedImageFormField(forms.MultiValueField):
    widget = CroppedImageWidget

    def __init__(self, *args, **kwargs):
        self.max_length = kwargs.pop('max_length', None)
        fields = (
            forms.ImageField(required=False),
            forms.CharField(required=False),
            forms.CharField(required=False),
            forms.CharField(required=False),
            forms.CharField(required=False),
            forms.CharField(required=False),
        )
        super(CroppedImageFormField, self).__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        if data_list[5]:
            tmp_image = TempImage.objects.get(pk=data_list[5])
            image = Image.open(tmp_image.image.path)

            if image.mode != "RGB":
                image = image.convert("RGB")

            x = int(data_list[1])
            y = int(data_list[2])
            w = int(data_list[3])
            h = int(data_list[4])
            crop = image.crop((x, y, x + w, y + h))

            name = tmp_image.image.name
            data = crop.tostring('jpeg', 'RGB')
            content_type = 'image/jpg'
            return SimpleUploadedFile(name.split('.')[-2], data, content_type)
        else:
            return data_list[0]



class CroppedImageField(ImageField):

    
    def formfield(self, **kwargs):
        defaults = {'form_class': CroppedImageFormField}
        defaults.update(kwargs)
        return super(CroppedImageField, self).formfield(**defaults)
