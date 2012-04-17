from django import forms
from django.conf import settings
from django.core.urlresolvers import reverse
from django.forms.widgets import ClearableFileInput, CheckboxInput
from django.utils.encoding import force_unicode
from django.utils.html import escape, conditional_escape
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy

if settings.DEBUG:
    JQUERY_URL = 'jcrop/js/jquery.min.js'
else:
    JQUERY_URL = 'http://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js'


class ViewableClearableFileInput(ClearableFileInput):

    initial_text = ugettext_lazy('Currently')
    input_text = ugettext_lazy('Change')
    clear_checkbox_label = ugettext_lazy('Clear')

    template_with_initial = u'''
                             <div>%(initial_text)s: %(initial)s</div>
                             <div>%(clear_template)s</div>
                             <div>%(input_text)s: %(input)s</div>
                             '''

    template_with_clear = u'<label for="%(clear_checkbox_id)s">%(clear_checkbox_label)s</label> %(clear)s'

    def render(self, name, value, attrs=None):
        substitutions = {
            'initial_text': self.initial_text,
            'input_text': self.input_text,
            'clear_template': '',
            'clear_checkbox_label': self.clear_checkbox_label,
        }
        template = u'%(input)s'
        substitutions['input'] = super(ClearableFileInput, self).render(name, value, attrs)

        if value and hasattr(value, "url"):
            template = self.template_with_initial
            substitutions['initial'] = (u'<a href="%s"><img src="%s"></img></a>'
                                        % (escape(value.url),
                                           escape(value.url),))
            if not self.is_required:
                checkbox_name = self.clear_checkbox_name(name)
                checkbox_id = self.clear_checkbox_id(checkbox_name)
                substitutions['clear_checkbox_name'] = conditional_escape(checkbox_name)
                substitutions['clear_checkbox_id'] = conditional_escape(checkbox_id)
                substitutions['clear'] = CheckboxInput().render(checkbox_name, False, attrs={'id': checkbox_id})
                substitutions['clear_template'] = self.template_with_clear % substitutions

        return mark_safe(template % substitutions)



class CroppedImageWidget(forms.MultiWidget):

    class Media:
        js = (
                    JQUERY_URL,
                    'fileupload/js/vendor/jquery.ui.widget.js',
                    'fileupload/js/jquery.iframe-transport.js',
                    'fileupload/js/jquery.fileupload.js',
                    'jcrop/js/jquery.Jcrop.min.js',
                    'djcrop/js/djcrop.js',
              )
        css = {
               'all': (
                       'djcrop/css/djcrop.css',
                       'jcrop/css/jquery.Jcrop.css',
                       )
        }

    def __init__(self, attrs=None):
        self.ratio = 0
        if attrs:
            self.ratio = attrs.pop('ratio', 0)
        widgets = (
            ViewableClearableFileInput(attrs=attrs), #image
            forms.HiddenInput(attrs=attrs), #x
            forms.HiddenInput(attrs=attrs), #y
            forms.HiddenInput(attrs=attrs), #w
            forms.HiddenInput(attrs=attrs), #h
            forms.HiddenInput(attrs=attrs), #temp image ID
            forms.HiddenInput(attrs=attrs), # File exists (for validation)
        )
        super(CroppedImageWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return [value, '', '', '', '', '', value.instance.id]
        return ['', '', '', '', '', '', '']

    def render(self, name, value, attrs=None):
        rendered = super(CroppedImageWidget, self).render(name, value, attrs)
        return mark_safe('''<div class="djcrop" id="id_%s">
                                <div>
                                    %s
                                    %s
                               </div>
                           </div>
                        ''' % (name,
                       rendered,
                       '''<script type="text/javascript">
                                    var UPLOAD_PATH = '%s';
                                    $('#id_%s').djCrop({
                                        ratio: %s
                                    });
                                    </script>''' % (reverse('save_tmp_image'), name, self.ratio)
                       )
                    )
