from django.conf.urls import url

from tsuru_autoscale.wizard import views


urlpatterns = [
    url(r'^(?P<instance>[\w-]+)/$', views.Wizard.as_view(), name='wizard-new'),
    url(r'^(?P<instance>[\w-]+)/remove/$', views.WizardRemove.as_view(), name='wizard-remove'),
    url(r'^(?P<instance>[\w-]+)/enable/$', views.WizardEnable.as_view(), name='wizard-enable'),
    url(r'^(?P<instance>[\w-]+)/disable/$', views.WizardDisable.as_view(), name='wizard-disable'),
    url(r'^$', views.Wizard.as_view(), name='wizard-new'),
]
