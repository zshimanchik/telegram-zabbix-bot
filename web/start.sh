python3 /app/manage.py collectstatic --noinput
python3 /app/manage.py migrate --noinput
uwsgi --socket=:3031 \
      --processes=1 \
      --harakiri=60 \
      --max-requests=10000 \
      --post-buffering=8192 \
      --wsgi-file=/app/smartsub/wsgi.py \
      --master \
      --pidfile=/tmp/uwsgi.pid \
      --vacuum \
      --die-on-term \
      --disable-logging \
      --logdate \
      --log-5xx \
      --log-slow=5000
