from django.conf.urls import patterns, url

from website import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^login$', views.login, name='login'),
    url(r'^customer_create$', views.customer_create, name='customer_create'),
    url(r'^customer_account$', views.customer_account, name='customer_account'),

    url(r'^add_command$', views.add_command, name='add_command'),
)