from xml.dom import NotFoundErr
from dotenv import load_dotenv
from flask import Flask, render_template
from flask_cors import CORS
from werkzeug import exceptions

load_dotenv()

from models.alligator import Alligator

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/alligators")
def show_alligators():

    alligators = [a.to_dict() for a in Alligator.get_all()]

    return render_template("alligators.html", alligators=alligators)

@app.route("/alligators/<int:id>")
def interact_with_alligator(id):
    try:
        alligator = Alligator.get_one_by_id(id).to_dict()
        return render_template("alligator.html", alligator=alligator)
    except NotFoundErr as err:
        raise exceptions.NotFound

@app.errorhandler(exceptions.NotFound)
def page_not_found(err):
    return render_template("404.html", error=err)

if __name__ == "__main__":
    app.run(debug=True)