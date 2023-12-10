from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import UserCreationForm
from django.urls import include, path
from django.views.generic import CreateView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

urlpatterns = [
    path('api/', include('api.urls')),
    path('', include('news.urls')),
    path('admin/', admin.site.urls),
]

auth_urls = ([
    path(
        'login/',
        auth_views.LoginView.as_view(),
        name='login',
    ),
    path(
        'logout/',
        auth_views.LogoutView.as_view(
            template_name='registration/logout.html'
        ),
        name='logout',
    ),
    path(
        'signup/',
        CreateView.as_view(
            form_class=UserCreationForm,
            success_url='/',
            template_name='registration/signup.html',
        ),
        name='signup'
    ),
], 'users')

urlpatterns += [path('auth/', include(auth_urls))]

schema_view = get_schema_view(
    openapi.Info(
        title="YaNews API",
        default_version='v1',
        description="Документация для приложения news проекта YaNews",
        contact=openapi.Contact(email="admin@kittygram.ru"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
    url(r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'),
]
