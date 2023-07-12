from flask import Flask, render_template, request, redirect, url_for
from redis_function import RedisHandler
import ulid


app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def upload_document():
    """
    Handles the upload of a document and enqueues it for processing.

    Returns:
        str: If the request method is 'POST', it redirects to the 'get_results' endpoint.
             Otherwise, it renders the Jinja template for document upload.
    """
    if request.method == "POST":
        document = request.files["document"]
        k = int(request.form["k"])
        id = ulid.new().timestamp().str
        redis_handler = RedisHandler()
        redis_handler.enqueue(id, k, document.read())
        return redirect(url_for("get_results", id=id))

    return render_template("upload.html")


@app.route("/result/<id>", methods=["POST", "GET"])
def get_results(id):
    """
    Retrieves the results associated with an ID and renders the results template.

    Args:
        id (str): The ID to retrieve the results for.

    Returns:
        str: The rendered HTML template with the results.

    """
    if request.method == "POST":
        redis_handler = RedisHandler()
        output = -1
        if redis_handler.key_exists(id):
            output = redis_handler.get_output(id)
        return render_template("results.html", id=id, output=output)

    return render_template("results.html", id=id, output=None)
