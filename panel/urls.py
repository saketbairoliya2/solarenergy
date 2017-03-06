from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.get_expected_data, name='get_expected_data'),
]