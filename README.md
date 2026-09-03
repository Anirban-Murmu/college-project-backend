# library 
Django==6.1
djangorestframework==3.18.0
djangorestframework_simplejwt==5.5.1
pillow==12.3.0
twilio==9.11.0
python-decouple==3.8
drf-spectacular==0.30.0
psycopg2-binary==2.9.12
django-cors-headers==4.9.0
cloudinary==1.46.2
jango-cloudinary-storage==0.3.0
gunicorn==26.2.0
uvicorn==0.52.4


# command
python -m venv env
.\env\Scripts\activate.ps1  
pip install django
pip install djangorestframework
pip install djangorestframework-simplejwt
pip install pillow
pip install twilio
django-admin stratproject config .

python manage.py startapp accounts

pip install python-decouple
pip install drf-spectacular
pip install django-cors-headers
pip install psycopg2-binary
pip install cloudinary django-cloudinary-storage

pip install  uvicorn 
pip install  gunicorn

# secret key generator 

python manage.py shell

from django.core.management.utils import get_random_secret_key
get_random_secret_key()





