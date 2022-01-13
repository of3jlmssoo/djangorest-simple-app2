https://realpython.com/django-social-network-1/ を基にしている。

python -m venv dsoc
source ./dsoc/bin/activate
python -m pip install django

django-admin startproject social .
python manage.py startapp dwitter

edit socal/settings.py to include dwitter as an installed apps

python manage.py migrate
python manage.py createsuperuser

- socialadmin
- socialadmin@mailz.com
- socadminial

python manage.py runserver

edit dwitter/admin.py to unregister the Group model and
change fields displayed on the panel
テスト目的のため簡素化

パネルからユーザー登録 alice and bob

1. フォローしている
2. フォローされている
3. dweets
   Profile モデル
   1：多 foreignkey
   1:1 onetoone
   多:多 manytomany
   models.py 編集

python manage.py makemigrations
python manage.py migrate

admin.py 更新

admin.py 更新 user と profile をまとめて処理

secret key exposed
settings.py

- environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
- SECRET_KEY = env('SECRET_KEY')
- DEBUG = env('DEBUG')

.env
SECRET_KEY=XXXXXXXXXXXXXXXXXXXXXXX
DEBUG=True

include .env in .gitignore
python -m pip install django-environ
