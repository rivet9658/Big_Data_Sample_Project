#!/bin/bash

# 等待資料庫就緒
while ! true >/dev/tcp/db/3306; do
  echo "Waiting for the database to be ready..."
  sleep 1
done

# 資料遷移
python manage.py makemigrations
python manage.py migrate

# 創建超級使用者
echo "from django.contrib.auth.models import User; User.objects.create_superuser('superadmin', 'superadmin@gmail.com', '1qaz@WSX3edc')" | python manage.py shell

exec "$@"
