from django.conf.urls import patterns, include, url
from tastypie.api import Api
from tracker.api import UserResource, TaskResource, WorkSessionResource, \
    ApiTokenResource
from tracker.views import SignupView

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

# tracker API.
v1_api = Api(api_name='v1')
v1_api.register(ApiTokenResource())
v1_api.register(UserResource())
v1_api.register(TaskResource())
v1_api.register(WorkSessionResource())

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^signup/', SignupView.as_view(), name='signup'),
    url(r'^api/', include(v1_api.urls)),
)
