--------------------　環境構築　--------------------

Djangoの環境構築にはAnacondaNavigatorを使用しております。


作成手順

    １：AnacondaNavigatorを開きEnvironmentsを押す
    
    ２：Createを押しr-drf-basic-backという仮想環境を作成（Pythonは3.7）
    
    ３：作成した環境の矢印からOpenTerminalへ移動しDjango DjangoRestFrameworkをインストールする
        ①： pip install django==3.0.7
        ②： pip install djangorestframework==3.10
        ③： pip install djangorestframework-simplejwt==4.1.2
        ④： pip install djoser
        ⑤： pip install django-cors-headers
        ⑥： pip install Pillow


PyCharmにAnacondaNavigatorで作成した仮想環境を紐づけ

    １：PyCharmのOpenProjectからフォルダを選択(今回だとdesktop/FSComics/fscomics-backから)
    
    ２：右上のPyCharm → Preferences →  → Project →  → ProjectInterpreter → 
        右上の歯車マーク → add.. → Existing environment → 右にある　... →
        Users → embeddedtech → opt → anaconda3 → envs →
        作成した仮想環境(今回ならfscomics) → bin → python を選択してOK
        
        
DjangoProject/DjangoAppの作成

    １：PyCharm上からターミナルを開く
    
    ２：DjangoProjectとDjangoAppを作成する
        ①：django-admin startproject fscomics_back .
        ②：django-admin startapp api
        
    ３：fscomics_backのmanage.pyを右クリックしてRunのところを押下する
    
    ４：右上の下矢印が書いてあるボタンからEditConfigurations...を押下する
    
    ５：Parameters:のところにrunserverと記載しOKを押す
    
    右上の「→」と「□」でサーバーのstart/stopができる様になる
    
    
DBとのやりとり

modelで定義してadminで登録処理を記載したらターミナルに移り

(models.py,記載後makemigrations/migrateができ、admin.py記載後superuserの作成ができる)

    1:マイグレーションファイルを作る（仮想的に）
        python manage.py makemigrations
    
    2:migrateする
        python manage.py migrate
        
    3:superuserの作成
        python manage.py createsuperuser
        Username: super
        Email address: super@gmail.com  (空白でもOK)
        Password: super
        Password (again): super
        
    本来パスワードはセキュアに設定し内密に自分で管理する事



Gitに関して（メモ用として必要最低限のものだけを記載）

    まず初めに行う事
    git init
    
    ブランチを切ってそのブランチの中に入る
    git checkout -b branch名
    
    追加した内容を全て加える（個別に加えたい場合はファイルを指定する事）
    git add -A
    
    addで加えて内容をステージング環境に上げる
    git commit -m 'コミット内容'
    
    マスターブランチに移動する
    git checkout master
    
    マスターブランチにブランチをmergeする
    git merge branch名
    
    リモートのリポジトリ（今回ならGitHub）にpushする
    git push -u origin master
    
    どんなブランチがあり自分がどのブランチにいるかの確認をする
    git branch
    
    
データベースをもう一度立て直したい時

    https://qiita.com/riz666/items/59352c336398e0321fc2
    appの部分は各自のアプリ名に変える事
    
    cd api
    rm -d -r migrations/
    
    cd ..
    rm -d -r db.sqlite3
    
    python manage.py makemigrations api
    
    python manage.py migrate
    
    python manage.py createsuperuser

    


備考

    ここのSerializerはフロントからの値を受け取り精査する場所
    今回ReviewSerializerにbookName,contentを追加しているのでReact側から値を渡す時に注意が必要
    
    Why??　　adminで作成したuserがReact側で表示されない理由
    userを作っただけでProfileを作成していないから、Profile情報がないよと拒否されてしまう
    
    

AWS接続にあたり

    環境変数、データベースの設定を簡単に扱えるようにする為のモジュール
    pip install django-environ
    pip install dj-database-url
    