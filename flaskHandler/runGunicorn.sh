gunicorn -w 4 -b 127.0.0.1:8093 wsgi --reload &
service nginx restart

