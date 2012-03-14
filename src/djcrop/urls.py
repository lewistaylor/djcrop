from django.conf.urls.defaults import patterns, url
from djcrop.views import SaveTempImageView

urlpatterns = patterns('',
    url(r'^save/$', SaveTempImageView.as_view(), name='save_tmp_image'),
)
