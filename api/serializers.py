from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Profile, Review, Comment


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        # get_user_model()はDjango標準の関数でactiveなUserを取得する
        model = get_user_model()

        # serializerで扱いたいパラメーターの一覧を記述する
        fields = ('id', 'email', 'password')

        # パラメータの属性を指定する。（今回はパスワードは読み取られる事がないようにwrite_onlyにしている）
        extra_kwargs = {'password': {'write_only': True}}

    # 登録した際にemailとpasswordが問題なく記載されればvalidated_dataはバリデーションを通った後のデータとして引数として渡される
    def create(self, validated_data):

        # UserManagerクラスのメソッドを使用できるobjectsを使用してcreate_userを呼び出している
        user = get_user_model().objects.create_user(**validated_data)
        return user


class ProfileSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)

    class Meta:
        model = Profile
        fields = ('id', 'nickName', 'userProfile', 'created_at', 'avatar')
        extra_kwargs = {'userProfile': {'read_only': True}}


class ReviewSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'title', 'bookName', 'content', 'userReview', 'created_at', 'img', 'likedUser')
        extra_kwargs = {'userReview': {'read_only': True}}


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'text', 'userComment', 'review')
        extra_kwargs = {'userComment': {'read_only': True}}


