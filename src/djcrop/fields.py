from PIL import Image
from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models.fields.files import ImageField
from django.forms.util import ErrorList
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

    def clean(self, value):
        """
        Validates every value in the given list. A value is validated against
        the corresponding Field in self.fields.

        For example, if this MultiValueField was instantiated with
        fields=(DateField(), TimeField()), clean() would call
        DateField.clean(value[0]) and TimeField.clean(value[1]).
        """
        clean_data = []
        errors = ErrorList()
        if not value or isinstance(value, (list, tuple)):
            if not value or not [v for v in value if v not in validators.EMPTY_VALUES]:
                if self.required:
                    raise ValidationError(self.error_messages['required'])
                else:
                    return self.compress([])
        else:
            raise ValidationError(self.error_messages['invalid'])

        if value[0]:
            try:
                field_value = value[0]
            except IndexError:
                field_value = None
            if self.required and field_value in validators.EMPTY_VALUES:
                raise ValidationError(self.error_messages['required'])
            try:
                clean_data.append(self.fields[0].clean(field_value))
            except ValidationError, e:
                # Collect all validation errors in a single list, which we'll
                # raise at the end of clean(), rather than raising a single
                # exception for the first error we encounter.
                errors.extend(e.messages)

            clean_data.extend([None for i in range(5)])
        else:
            clean_data = [None, ]
            for i, field in enumerate(self.fields[1:]):
                try:
                    field_value = value[i + 1]
                except IndexError:
                    field_value = None
                if self.required and field_value in validators.EMPTY_VALUES:
                    raise ValidationError(self.error_messages['required'])
                try:
                    clean_data.append(field.clean(field_value))
                except ValidationError, e:
                    # Collect all validation errors in a single list, which we'll
                    # raise at the end of clean(), rather than raising a single
                    # exception for the first error we encounter.
                    errors.extend(e.messages)
            if errors:
                raise ValidationError(errors)

        out = self.compress(clean_data)
        self.validate(out)
        return out

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
            tmp_image.image.delete()
            tmp_image.delete()
            return SimpleUploadedFile(name.split('.')[-2] + '.jpg', data, content_type)
        else:
            return data_list[0]



class CroppedImageField(ImageField):


    def formfield(self, **kwargs):
        defaults = {'form_class': CroppedImageFormField}
        kwargs['widget'] = CroppedImageWidget
        defaults.update(kwargs)
        return super(CroppedImageField, self).formfield(**defaults)
