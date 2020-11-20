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




"""
シリアライザーの概念
    クライアント側のjson形式のデータとDBのModelオブジェクトを相互に変換する際に使用される
    ( json  ←←←  serializer  →→→  ModelObject )
    その際に属性を付与してあげるとセキュリティ性が上がる（例えばread_onlyにしてあげると書き換えはできなくなり、データ参照だけが可能になるとか）
    
    クライアントからデータを受け取る際にmodels.pyに指定した、最大文字数(max_length)や値の重複を許さない(unique)などのバリデーションをかけ
    バリデーションが通ったデータをvalidated_dataという辞書型のデータに入れてDBへ渡す（バリデーションがかからない時は空のデータとなる）
    models.pyに blank=True, null=True 等の記載がない場合、値が渡されないとエラーが出る
    

シリアライザーの記述の仕方
    
    基本的にはmodels.pyで作成したmodelごとに作成していく事が多い。（例外はもちろんあり）
    
    class Meta:　　オプションを書く場所
        modelの横にserializerの元になるモデルを定義する
            get_user_modelはDjangoの標準の関数で現在アクティブなuserを取ってくる
        feildは取り扱いたいパラメータの一覧を記載する
        extra_kwargsのところに属性（read_onlyなど）を記載する
        
    def create(self, validated_data):　受け取った値が問題なければvalidated_dataに辞書型で入ってくる
        user = get_user_model().objects.create_user(**validated_data)
        シリアライザーに定義したモデルのcreate_userメソッドを使用して引数として渡されたvalidated_dataを使いデータをDBに保存する
        objectsはUserManagerをオーバーライドしたメソッドでUserManagerで定義されているメソッドを使用できる
    
    
    
    extra_kwargs = {'userProfile': {'read_only': True}}
    extra_kwargs = {'userReview': {'read_only': True}}
    extra_kwargs = {'userComment': {'read_only': True}}
    これらはViews.pyでログインしているユーザーを自動で割り当てる為に使用する
    投稿するのにユーザーが動作をするのかを認識するのにユーザー名、emailなどを入れる手間を省く為

"""