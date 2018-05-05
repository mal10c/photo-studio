import time
import redis
from flask import Flask

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

def get_hit_count():
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
    count = get_hit_count()

    html = """
        <iframe width="0" height="0" border="0" name="dummyframe" id="dummyframe"></iframe>
        <form action="http://0.0.0.0:5002" method="get" target="dummyframe">
            <input type="submit" value="take pic"/>
        </form>"
        """

    return html + '\nWoot hi!  I have been seen {} times.\n'.format(count)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

