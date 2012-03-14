from django import forms


class CroppedImageWidget(forms.MultiWidget):

    def __init__(self, attrs=None):
        widgets = (
            forms.ClearableFileInput(attrs=attrs),
            forms.HiddenInput(attrs=attrs),
            forms.HiddenInput(attrs=attrs),
            forms.HiddenInput(attrs=attrs),
            forms.HiddenInput(attrs=attrs),
            forms.HiddenInput(attrs=attrs),
        )
        super(CroppedImageWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return value.split(':::')[0:2]
        return ['', '']
