from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
    url(r'^$', views.manifest_upload, name='manifest-upload'),
    url(r'^upload/(?P<manifest_id>\d+)$', views.media_file_upload, name='file-upload'),
    url(r'^manifest/(?P<manifest_id>\d+)$', views.manifest_view, name='manifest-view'),
    url(r'^download/(?P<media_file_id>\d+)$', views.media_file_download, name='file-download'),
)
