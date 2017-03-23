from django.conf.urls import url

from . import views

urlpatterns = [
	# /panel/
    url(r'^$', views.index, name='index'),
    # /panel/1
    url(r'^(?P<panel_id>[0-9]+)$', views.details, name='details'),
    # /panel/1/mail
    url(r'^(?P<panel_id>[0-9]+)/mail$', views.send_daily_mail, name='send_daily_mail'),
    # /panel/call
    url(r'^call$', views.prepare_daily_mail, name='prepare_daily_mail'),
]