from django.http import HttpResponse
from django.utils import simplejson
from django.views.generic.edit import CreateView
from djcrop.forms import TempImageForm


class SaveTempImageView(CreateView):

    form_class = TempImageForm

    def form_valid(self, form):
        self.object = form.save()

        data = [
          {
            "name":self.object.image.name,
            "size":len(self.object.image),
            "url":self.object.image.url,
            "thumbnail_url":self.object.image.url,
            "id":self.object.id,
          }
         ]

        response = simplejson.dumps(data)
        return HttpResponse(response)

    def form_invalid(self, form):
        return HttpResponse(form.errors)

