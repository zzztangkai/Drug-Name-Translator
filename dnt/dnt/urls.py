from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin

from cropapp import views
from login import views as loginviews
from searchapp import views as vs
from searchapp.views import SearchView

urlpatterns = [
    url(r'admin/', admin.site.urls),
    url(r'^register/$', loginviews.register, name='register'),
    url(r'^confirm/$', loginviews.user_confirm),
    url(r'reset/$',loginviews.pwd_reset,name='reset'),

    url(r'^$', loginviews.login, name='login'),
    url(r'^logout/$', loginviews.logout, name='logout'),
    url(r'^forget/$', loginviews.forget, name="forget"),
    url(r'^account_details/$', loginviews.account_deails, name="account_details"),
    url(r'^update_details/$', loginviews.update_details, name="update_details"),
    url(r'^update_pass/$', loginviews.update_pass, name="update_pass"),
    url(r'^contact_us/$', loginviews.contact_us, name="contact_us"),
    url(r'^help/$', loginviews.help, name="help"),
    
    url(r'^cropimage/$', views.crop_view, name='crop_view'),
    url(r'^search$', SearchView.as_view(), name='search_view'),
    url(r'^clear/$', vs.clear_history_view, name='clear_history_view'),
    url(r'^translate/(?P<filename>[\w\-\_ ]+)/$', vs.translate_view, name='translate_view'),
    url(r'^didyoumean/(?P<link>[\w\-\_ ]+)/$', vs.did_you_mean_view, name='did_you_mean_view'),
    url(r'^moreinfo/(?P<search_term>[\w&(),-_.?<>@!#$^*+|~`;:/+ ]+)/$', vs.more_info_view, name='more_info_view'),
    url(r'^history/(?P<history_term>[\w\-\_ ]+)/$', vs.history_view, name='history_view'),
    url(r'^(?P<filename>[\w]+)/(?P<link>[\w\-\_]+)/$', vs.link_display_view, name='link_display_view'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
