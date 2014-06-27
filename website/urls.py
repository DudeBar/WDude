from django.conf.urls import patterns, url

from website import views

urlpatterns = patterns(
    '',
    url(r'^$', views.home, name='home'),
    url(r'^actu$', views.actu, name='actu'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^login$', views.login, name='login'),
    url(r'^customer_create$', views.customer_create, name='customer_create'),
    url(r'^customer_account$', views.customer_account, name='customer_account'),

    url(r'^add_command$', views.add_command, name='add_command'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'bar_login.html'},
        name='bar_login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
    url(r'^add_fidelity/(?P<customer_id>\d+)/$', views.add_fidelity, name='add_fidelity'),
    url(r'^add_fidelity/$', views.new_fidelity, name='new_fidelity'),
    url(r'^bade_fidelity$', views.bade_fidelity, name='bade_fidelity'),

    url(r'^barman_account$', views.barman_account, name='barman_account'),
    )