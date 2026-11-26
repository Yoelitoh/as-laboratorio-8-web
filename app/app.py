"""Aplicacion web con contador de visitas usando Flask y Redis."""
import time
import redis
from flask import Flask

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)


def get_hit_count():
    """Incrementa y devuelve el contador de visitas."""
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)


@app.route('/')
def hello():
    """Pagina principal con el contador."""
    count = get_hit_count()
    return f'Hola desde la rama nueva! Visitas: {count}\n'
