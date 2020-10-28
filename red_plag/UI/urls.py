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
	path('welcome/', v.login1, name='welcome'),
	path('signup/', v.signup, name='signup'),
	path('save/', v.save, name='save'),
	path('saved/', v.loggedin, name='saved'),
	path('home/', v.logoutin, name='home'),
	path('change/', v.change, name='change'),
	path('pass/', v.password, name='password'),
	path('loghome/', v.loghome, name='loghome'),
	path('yourfiles/', v.yourfiles, name='files'),
	url(r'^download/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
	path('organization/', v.orga, name='org'),
	path('orgaa/', v.org, name='orgaa'),
	path('<str:temp>/', v.temporary, name='connection'),
#	url(r'^login/(?P<username>[^/]+)/(.*)?', RedirectView.as_view(pattern_name='login')),
#	url(r'^login/$', RedirectView.as_view(pattern_name='login')),
#	path('connection/', v.login, name='connection'),
]
if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
