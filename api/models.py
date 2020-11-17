from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings

# デフォルトではDjangoでUserという雛形のクラスが定義されていて
# 認証にusernameとpasswordを使用するが、今回はemailとPasswordにするため
# Overrideしてemailで認証できるようにカスタマイズをする。



# 継承する場合はカッコの中に継承したいクラスを記載する
class UserManager(BaseUserManager):

    # create_userはDjangoのBaseUserManagerに元々入っている機能
    # 通常はusernameだが今回はemailで認証できるように引数にemailを入れている
    def create_user(self, email, password=None):

        # 例外処理でemailがない場合は「emailが必要です」という例外を出す
        if not email:
            raise ValueError('emailが必要です')

        # modelというメソッドを使用してインスタンスを作りuserという箱に入れている
        # normalize_emailはemailの正規化を行っている（emailは小文字で扱われるので小文字に変えている）
        user = self.model(email=self.normalize_email(email))

        # Djangoの裏側でパスワードをハッシュ化してから入れるという設定になっている
        user.set_password(password)

        # 作ったuserというインスタンスをDBに保存する
        user.save(using=self._db)

        return user


    # Djangoではsuperuserというものを作れるがcreate_userをカスタマイズした場合は
    # superuserもカスタマイズする必要がある
    def create_superuser(self, email, password):

        # 上で作成したcreate_userメソッドを使用してuserインスタンスを作成する
        user = self.create_user(email, password)

        # いくつかの権限がありActive,Staff,SuperUserという権限がある
        # ①　ActiveはT/Fでアカウントの有効/無効が切り替えられ無効になるとログインできなくなる
        # ②　StaffはT/FでAdminのダッシュボードにログインする権限（ログインしてデータを見るだけ）
        # ③　SuperUserはでAdminのダッシュボードにログインしDB内容などを変更する事が出来る（全権限）
        user.is_staff = True
        user.is_superuser = True

        # 作ったuserというインスタンスをDBに保存する
        user.save(using=self._db)

        return user



# あらかじめDjangoで用意されているUserをOverrideして使用している
# 今回はAbstractBaseUserとPermissionsMixinの2つのクラスをオーバーライドしている
class User(AbstractBaseUser, PermissionsMixin):

    # emailを使用するのでUserモデルに新しく属性として付与している
    # 最大50文字までとユニークな値でないと登録できないような設定にしている
    email = models.EmailField(max_length=50, unique=True)

    # このUserというクラスは実際のUserをイメージしているので、adminダッシュボードは見れないようにしておく
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # UserManagerクラスのメソッドを使用できるobjectインスタンスを作成している
    objects = UserManager()

    # デフォルトではusernameだが今回認証に使うのはemailのためオーバーライドしている
    USERNAME_FIELD = 'email'

    # emailを文字列として返すためにPythonの特殊関数を使用している
    def __str__(self):
        return self.email


#--------------------------------（プロフィールクラス）------------------------------------------


#　画像を保存するためにファイル名を整形する
def upload_avatar_path(instance, filename):

    #　.で区切ったファイル名の一番後ろつまり拡張子を取ってきてextに入れる（jpeg/png）
    ext = filename.split('.')[-1]

    #　avatarsフォルダの直下にUserモデルに紐づいたProfileインスタンスのid　＋　ProfileインスタンスのnickNameを繋げたファイルを作成する。
    return '/'.join(['avatars', str(instance.userId.id) + str(instance.nickName) + str(".") + str(ext)])



class Profile(models.Model):
    nickName = models.CharField(max_length=20)

    # DjangoのUserモデルとOne to Oneで結びつけており、
    # Userが削除されたらProfileも削除されるように設定している（on_delete）
    userId = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='userId', on_delete=models.CASCADE
    )

    #　Avatarを保存する（ただしblank,nullを許容して画像は任意とする）
    avatar = models.ImageField(blank=True, null=True, upload_to=upload_avatar_path)

    # Userインスタンスが作られた時に自動でその時の日時を入れてくれる
    createdAt = models.DateTiemField(auto_now_add=True)

    def __str__(self):
        return self.nickName



#--------------------------------（レビュークラス）------------------------------------------


def upload_review_path(instance, filename):
    ext = filename.split('.')[-1]
    return '/'.join(['reviews', str(instance.userId.id) + str(instance.title) + str(".") + str(ext)])

class Review(models.Model):
    title = models.CharField(max_length=100)
    bookName = models.CharField(max_length=100)
    content = models.TextField(max_length=1000)
    userId = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='userId', on_delete=models.CASCADE
    )
    img = models.ImageField(blank=True, null=True, upload_to=upload_review_path)
    likedUserId = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='likedUserId', blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title




#--------------------------------（コメントクラス）------------------------------------------

class Comment(models.Model):
    text = models.CharField(max_length=100)
    userId = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='userId',
        on_delete=models.CASCADE
    )
    postId = models.ForeignKey(Review, on_delete=models.CASCADE)

    def __str__(self):
        return self.text





