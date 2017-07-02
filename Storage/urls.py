from django.conf.urls import url
from Storage.views import index

urlpatterns = [
    url(r'^$', index, name='index'),
]