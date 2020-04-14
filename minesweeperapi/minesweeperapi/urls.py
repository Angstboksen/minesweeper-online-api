
from django.urls import include, path
from django.conf.urls import url
from django.contrib import admin
from rest_framework.authtoken.views import obtain_auth_token
from api import views

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include('api.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
    url(r'^api-token-auth/', views.CustomAuthToken.as_view()),
]
