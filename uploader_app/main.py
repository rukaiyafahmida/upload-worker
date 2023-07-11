from flask import Flask, render_template, request
from redis_functions import RedisHandler
import ulid


app = Flask(__name__)



@app.post('/')
def upload_document():
    if request.method == 'POST':
        # Handle document upload
        document = request.files['document']
        k = int(request.form['k'])
        id = ulid.new().timestamp().str
        queue = RedisHandler()
        queue.add_to_proccesing(id, k, document.read())
        return 'Document uploaded and queued for processing.'

    # Render the Jinja template for document upload
    return render_template('upload.html')