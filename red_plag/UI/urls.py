from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from django.conf.urls import url, include
from UI import views as v
from django.views.generic.base import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
urlpatterns = [
	path('',v.login1, name='connection'),
	path('forgotpassword1/', v.forgotpassword1, name='forgotpassword1'),
	path('forgotpassword2/', v.forgotpassword2, name='forgotpassword2'),
	path('resetpassword/', v.resetpassword, name='resetpassword'),
	path('univsignup/', v.univsignup, name='univsignup'),
	path('<str:username>/dashboard/',v.dashboard,name='dashboard'),
	path('<str:username>/univdashboard/',v.univdashboard,name='univdashboard'),
	path('signup/', v.signup, name='signup'),
	path('createdaccount/', v.createdaccount, name='createdaccount'),
	path('univcreatedaccount/', v.univcreatedaccount, name='univcreatedaccount'),
	path('<str:username>/uploadfiles/', v.uploadfiles, name='uploadfiles'),
	path('home/', v.logout1, name='home'),
	path('<str:username>/changepassword/', v.changepassword, name='changepassword'),
	path('<str:username>/univchangepassword/', v.univchangepassword, name='univchangepassword'),
	path('<str:username>/savepassword/', v.savepassword, name='savepassword'),
	path('<str:username>/univsavepassword/', v.univsavepassword, name='univsavepassword'),
	path('<str:username>/changepasscode/', v.changepasscode, name='changepasscode'),
	path('<str:username>/savepasscode/', v.savepasscode, name='savepasscode'),
	path('<str:username>/yourfiles/', v.yourfiles, name='files'),
	path('<str:username>/<str:filepath/', v.download_file, name='result'),
	path('<str:univ>/<str:username>/univfiles/', v.univfiles, name='univfiles'),
	url(r'^download/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
	path('<str:temp>/', v.temporary, name='connection'),
	path('<str:temp1>/<str:temp2>/', v.temporary1, name='connection'),
        path('<str:temp1>/<str:temp2>/<str:temp3>/', v.temporary2, name='connection'),
        url(r'^.*$', RedirectView.as_view(pattern_name='connection', permanent=False))
#	url(r'^/(?P<username>[^/]+)/(.*)?', RedirectView.as_view(pattern_name=v.login)),
#	url(r'^login/$', RedirectView.as_view(pattern_name='login')),
#	path('connection/', v.login, name='connection'),
]
if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
