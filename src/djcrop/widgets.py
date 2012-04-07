from django import forms
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe


class CroppedImageWidget(forms.MultiWidget):

    class Media:
        js = (
                    'http://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js',
                    'fileupload/js/vendor/jquery.ui.widget.js',
                    'fileupload/js/jquery.iframe-transport.js',
                    'fileupload/js/jquery.fileupload.js',
                    'jcrop/js/jquery.Jcrop.min.js',
                    'djcrop/js/djcrop.js',
              )
        css = {
               'all': (
                       'jcrop/css/jquery.Jcrop.css',
                       )
        }

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
            return ['', '']
            #return value.split(':::')[0:2]
        return ['', '']

    def render(self, name, value, attrs=None):
        rendered = super(CroppedImageWidget, self).render(name, value, attrs)
        return mark_safe('''<div class="djcrop" id="id_%s">
                    %s
                    %s
                   </div>
                ''' % (name,
                       rendered,
                       '''<script type="text/javascript">
                                    var UPLOAD_PATH = '%s';
                                    $('#id_%s').djCrop();
                                    </script>''' % (reverse('save_tmp_image'), name,)
                       )
                    )
