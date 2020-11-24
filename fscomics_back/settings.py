import os

# JWTを認証で使う際にTokenの認証期限設定できるモジュール
from datetime import timedelta

# 環境変数を扱う為のモジュール ○○○
import environ


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 環境変数（.env）ファイルを使用する為の追記 ○○○
env = environ.Env()
env.read_env(os.path.join(BASE_DIR, '.env'))

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'q@c%ie0^1yl-5y@h4-)dy1m(+rt3n15)kpx9q_$q6o9gkssst_'
# ○○○
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
# ○○○
DEBUG = env('DEBUG')

ALLOWED_HOSTS = []


# 使用するアプリケーションの定義

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 今回使用するアプリケーションを追記
    # rest_framework,djoser,corsheadersは環境構築の際にすでにインストールしてあり
    # api.apps.ApiConfigはcreateappで作成したapiフォルダのこと
    'rest_framework',
    'djoser',
    'api.apps.ApiConfig',
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # 今回使用するミドルウェアを追記
    'corsheaders.middleware.CorsMiddleware',
]

# corsを使用する際にReactからきたアクセスを許可するため定義
# firebaseデプロイ環境
CORS_ORIGIN_WHITELIST = [
    "https://fs-comics.web.app"
]
# ローカル開発環境
# CORS_ORIGIN_WHITELIST = [
#     "http://localhost:3000"
# ]





ROOT_URLCONF = 'fscomics_back.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'fscomics_back.wsgi.application'

# 認証系の定義（全てのViewに適用される、もし特定のViewは認証を通したく無い場合上書きをする必要がある）
REST_FRAMEWORK = {
    # ログインしているユーザーだけにViewの内容を見れるようにする定義
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    # 認証をどのように行うかの定義（今回はJWTAuthenticationの方法で行う）
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

# JWTの定義（サードパーティのModuleを使用）
SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('JWT',),
    # 認証する時間を定義しており今回だと120分経つと認証に必要なTokenが使えなくなる
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=120),
}




# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

# ○○○
DATABASES = {
    'default': env.db()
}



# Passwordのバリデーション validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization

LANGUAGE_CODE = 'en-us'

# 東京の時間に設定し直す
TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# 今回DjangoデフォルトのUserモデルではなく、models.pyでカスタマイズした
# Userモデルを使用するので、使いますと明示的に記載する(models.pyの58行目)
AUTH_USER_MODEL = 'api.User'


# staticフォルダの設定
STATIC_URL = '/static/'


# 投稿したAvatar画像やReviewの画像をどのフォルダに格納するかの定義

# BASE_DIR(デスクトップ配下のfscomics_backのディレクトリ)のmediaというフォルダに格納する
# まだmediaフォルダはないのでこのタイミングで作成しておくこと
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'



# AWSに接続する際に必要な設定
# adminダッシュボードは静的なstaticファイルの塊であり今回ダッシュボードを使用する為に
# staticというフォルダにまとめておくと言う設定が必要になる為記述
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
