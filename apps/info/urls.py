from django.contrib import admin
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings
from apps.info.views import index,upload,graphic
from django.conf.urls.static import static

urlpatterns = [
	url(r'^upload', upload),
	url(r'^graphic', graphic),
	url(r'^index', index),
    url(r'^$', index),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)

