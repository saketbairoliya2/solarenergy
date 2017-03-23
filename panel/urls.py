from django.conf.urls import url

from . import views

urlpatterns = [
	# /panel/
    url(r'^$', views.index, name='index'),
    # /panel/1
    url(r'^(?P<panel_id>[0-9]+)$', views.details, name='details'),
    url(r'^(?P<panel_id>[0-9]+)/send_mails/$', views.send_daily_mail, name='send_daily_mail'),
]