from flask import Flask
from flask_caching import Cache
from celery import Celery
from celery.result import AsyncResult
import time

app = Flask(__name__)

app.config['CACHE_TYPE'] = 'redis'
app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/1'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/2'

cache = Cache(app)
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'], backend=app.config['CELERY_RESULT_BACKEND'])
celery.conf.update(app.config)

@app.route('/data')
@cache.cached(timeout=60, key_prefix='cached_data')
def get_data():
    time.sleep(3) 
    return {"data": "Slow database result"}

@app.route('/update')
def update_data():
    cache.delete('cached_data') 
    return {"msg": "Data updated, cache cleared"}

@celery.task
def background_job():
    time.sleep(5)
    print("Background work finished")
    return "Done"

@app.route('/run')
def run_job():
    task = background_job.delay()
    return {"msg": "Job started", "task_id": task.id}

@app.route('/status/<task_id>')
def get_status(task_id):
    task_result = AsyncResult(task_id, app=celery)
    return {
        "task_id": task_id,
        "status": task_result.status,
        "result": task_result.result
    }

if __name__ == '__main__':
    app.run(debug=True)