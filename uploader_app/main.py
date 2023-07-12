from flask import Flask, render_template, request
from redis_function import RedisHandler
import ulid


app = Flask(__name__)



@app.route('/')
def upload_document():
    if request.method == 'POST':
        # Handle document upload
        document = request.files['document']
        k = int(request.form['k'])
        id = ulid.new().timestamp().str
        queue = RedisHandler()
        queue.proccesing_queue_push(id, k, document.read())
        return 'Document uploaded and queued for processing.'

    # Render the Jinja template for document upload
    return render_template('upload.html')

