# 第一次部屬會執行資料遷移及創建一超級使用者
if [ ! -f /.firstrun ]
then
	touch /.firstrun
    python manage.py makemigrations
    python manage.py migrate
    echo "from django.contrib.auth.models import User; User.objects.create_superuser('superadmin', 'superadmin@gmail.com', '1qaz@WSX3edc')" | python manage.py shell
fi
python manage.py runserver 0.0.0.0:8000