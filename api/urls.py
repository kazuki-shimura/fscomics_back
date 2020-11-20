from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

app_name = 'user'

# ModelViewSetを使用した場合はDefaultRouterを使用してどのUrlと紐付けをするか設定する
router = DefaultRouter()
router.register('profile', views.ProfileViewSet)
router.register('review', views.ReviewViewSet)
router.register('comment', views.CommentViewSet)

# 汎用のAPIViewを使用した場合はurlpatternsに記載してどのUrlと紐付けをするか設定する
urlpatterns = [
    path('register/', views.CreateUserView.as_view(), name='register'),
    path('myprofile/', views.MyProfileListView.as_view(), name='myprofile'),
    path('', include(router.urls)),
]


"""
path('myprofile/', views.MyProfileListView.as_view(), name='myprofile'),
これはReactの方では使わずDjangoでしか使用しない（Postman,adminのダッシュボード）
"""
