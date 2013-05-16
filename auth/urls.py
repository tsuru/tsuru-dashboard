from django.conf.urls import patterns, url

from auth import views


urlpatterns = patterns(
    '',
    url(r'^login/$', views.Login.as_view(), name='login'),
    url(r'^logout/$', views.Logout.as_view(), name='logout'),
    url(r'^key/$', views.Key.as_view(), name='key'),
    url(r'^signup/$', views.Signup.as_view(), name='signup'),
    url(r'^token-request/$', views.TokenRequest.as_view(),
        name='token-request'),
    url(r'^token-request/success/$', views.TokenRequestSuccess.as_view(),
        name='token-request-success'),
    url(r'^password-recovery/$', views.PasswordRecovery.as_view(),
        name='password-recovery'),
    url(r'^password-recovery-recovery/$',
        views.PasswordRecoverySuccess.as_view(),
        name='password-recovery-success'),
)
