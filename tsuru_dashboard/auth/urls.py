from django.conf.urls import url

import views


urlpatterns = [
    url(r'^login/$', views.Login.as_view(), name='login'),
    url(r'^logout/$', views.Logout.as_view(), name='logout'),
    url(r'^keys/add$', views.KeysAdd.as_view(), name='add-keys'),
    url(r'^keys/list$', views.KeysList.as_view(), name='list-keys'),
    url(r'^keys/remove/(?P<key>[\w-]+)$', views.KeysRemove.as_view(), name='remove-keys'),
    url(r'^signup/$', views.Signup.as_view(), name='signup'),
    url(r'^callback/$', views.Callback.as_view(), name='callback'),
    url(r'^token-request/$', views.TokenRequest.as_view(), name='token-request'),
    url(r'^token-request/success/$', views.TokenRequestSuccess.as_view(),
        name='token-request-success'),
    url(r'^password-recovery/$', views.PasswordRecovery.as_view(), name='password-recovery'),
    url(r'^password-recovery/success/$', views.PasswordRecoverySuccess.as_view(),
        name='password-recovery-success'),
    url(r'^change-password/$', views.ChangePassword.as_view(), name='change-password'),
]
