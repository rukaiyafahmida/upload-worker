from flask import Flask, render_template, request, redirect, url_for
from redis_function import RedisHandler
import ulid


app = Flask(__name__)



@app.route('/',methods = ['POST', 'GET'])
def upload_document():
    if request.method == 'POST':
        # Handle document upload
        document = request.files['document']
        k = int(request.form['k'])
        id = ulid.new().timestamp().str
        queue = RedisHandler()
        queue.proccesing_queue_push(id, k, document.read())
        return redirect(url_for('get_results', id=id))

    # Render the Jinja template for document upload
    return render_template('upload.html')

@app.route("/result/<id>", methods=['POST', 'GET'])
def get_results(id):
    if request.method == 'POST':
        redis_handler = RedisHandler()
        output = -1
        if redis_handler.key_exists(id):
            output = redis_handler.get_output(id)
        return render_template('results.html', id=id, output=output)
    
    return render_template('results.html', id=id, output=None)