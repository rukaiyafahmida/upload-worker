# from flask import Flask, render_template, request
# import redis



# redis_client = redis.Redis(host='localhost', port=6379)



# app = Flask(__name__)



# @app.route('/', methods=['GET', 'POST'])
# def upload_document():
#     if request.method == 'POST':
#         # Handle document upload
#         document = request.files['document']
#         k = int(request.form['k'])

#         # Store the document in Redis for processing
#         redis_client.rpush('documents', document.read())
#         redis_client.rpush('k_values', k)

#         return 'Document uploaded and queued for processing.'

#     # Render the Jinja template for document upload
#     return render_template('upload.html')




import ulid




id = ulid.new().timestamp().str
print(id)
