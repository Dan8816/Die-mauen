from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^create$', views.create),
    url(r'^success$', views.success),
    url(r'^success/post_msg$', views.create_msg),
    url(r'^success/post_cmnt$', views.create_cmnt),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
]