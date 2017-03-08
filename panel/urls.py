from django.conf.urls import url

from . import views

urlpatterns = [
	# /panel/
    url(r'^$', views.index, name='index'),
    # /panel/1
    url(r'^(?P<panel_id>[0-9]+)$', views.details, name='details'),
]