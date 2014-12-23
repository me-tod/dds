from django.conf.urls import patterns, url
from django.conf.urls.static import static

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
from edit import views

urlpatterns = patterns('',
    url(r'^$', views.index, name = 'index'),
    url(r'^api/list', views.list, name = 'list'),
    url(r'^api/rows', views.rows, name = 'rows'),
    url(r'^api', views.api, name = 'api'),
)

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
