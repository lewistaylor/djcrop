from django.conf import settings
from django.conf.urls.defaults import patterns, url, include
from django.contrib import admin
from django.views.generic.edit import CreateView
from tester.models import MyTest

# Uncomment the next two lines to enable the admin:
admin.autodiscover()

admin.site.register(MyTest)

urlpatterns = patterns('',

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    url('^$', CreateView.as_view(template_name='base.html',
                                                        model=MyTest), name='home'),
                       
    url('^djcrop/', include('djcrop.urls')),              
)

if settings.DEBUG:
    urlpatterns += patterns('',
            url(r'^%s(?P<path>.*)$' % (settings.MEDIA_URL[1:]),
                'django.views.static.serve',
                {'document_root': settings.MEDIA_ROOT,
                 'show_indexes': True, }
                ),
   )
