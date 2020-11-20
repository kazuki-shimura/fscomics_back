from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from . import serializers
from .models import Profile, Review, Comment

# 汎用のAPIViewを使用しているので.saveなどの記載が必要なくなる
# ここでは新規作成で元々データはないのでquerysetは必要がない
class CreateUserView(generics.CreateAPIView):
    serializer_class = serializers.UserSerializer
    permission_classes = (AllowAny,)


class ProfileViewSet(viewsets.ModelViewSet):
    # データを取得する為に必要なもの
    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileSerializer

    # serializerでuserProfileをread_onlyにしたのでオーバーライドする必要がある
    # perform_createとは新規で作成する時に使えるrest_frameworkの定義の1つ
    def perform_create(self, serializer):
        # .request.userで現在ログインしているuserをuserProfileに格納する事で
        # どのUserがプロフィールへの操作をしているのかを判断する事ができる
        serializer.save(userProfile=self.request.user)


class MyProfileListView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileSerializer

    def get_queryset(self):
        # filter内でログインしているuserだけを返すようfilterをかけている
        return self.queryset.filter(userProfile=self.request.user)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = serializers.ReviewSerializer

    def perform_create(self, serializer):
        serializer.save(userReview=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer

    def perform_create(self, serializer):
        serializer.save(userComment=self.request.user)


"""
DjangoRestframeworkのViewについて

    ModelViewSetと汎用のAPIView(複数)の２種類がある
    
    ModelViewSetはCRUDを全て使用する時に便利
    
    汎用のAPIViewはCRUDのどれかに特化した機能を使用したい時に使用する
        CreateAPIView, ListAPIView, DestroyAPIView, UpdateAPIView　などなど
        
    汎用のViewを使用する際　・・・　generics
    CRUDを全て使用する際　・・・・　ModelViewSet
    
    
    AllowAny　・・・　今回settings.pyで全ての動作にJWTの認証を必要としている。
    しかし新規ユーザーを作る際まだその人はuserデータを持っていないのでJWTを取得できない
    そこでAllowAnyで上書きする事で、指定したViewではどんなuserでもアクセスできるようにする
"""