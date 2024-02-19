Install django-rlists
=====================


## Download and Install
```
git clone https://github.com/patrickwayodi/django-rlists.git
cd django-rlists
python3 -m venv ~/virtualenvs/rlistsvenv
source ~/virtualenvs/rlistsvenv
pip install --upgrade pip wheel
pip install --upgrade -r requirements.txt
nano core/settings.py
INSTALLED_APPS = [
    ...
    'apps.rlists',
]
nano core/urls.py

urlpatterns = [
    ...
    path('rlists/', include('apps.rlists.urls')),
]
python manage.py makemigrations rlists
python manage.py migrate
python manage.py loaddata fide_rating_list.json
python manage.py runserver --port 8000
firefox http://localhost:8000/rlist
```

