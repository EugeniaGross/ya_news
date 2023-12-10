from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import SimpleRouter

from .views import CommentViewSet, NewViewSet

app_name = 'api'

router = SimpleRouter()
router.register(
    'news',
    NewViewSet,
    basename='news'
)
router.register(
    r'news/(?P<news_id>\d+)/comment',
    CommentViewSet,
    basename='comment'
)

urlpatterns = [
    path('v1/', include((router.urls))),
    path('v1/api-token-auth/', views.obtain_auth_token),
    path('v1/auth/', include('djoser.urls')),
    path('v1/auth/', include('djoser.urls.jwt')),
    path('v1/api-auth/', include('rest_framework.urls'))
]
