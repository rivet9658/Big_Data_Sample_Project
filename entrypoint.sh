#!/bin/bash

# 資料遷移
python manage.py makemigrations
python manage.py migrate

# 是否要創建超級使用者
echo "from django.contrib.auth.models import User; User.objects.create_superuser('superadmin', 'superadmin@gmail.com', '1qaz@WSX3edc')" | python manage.py shell

# 執行您的應用程序或其他命令
exec "$@"