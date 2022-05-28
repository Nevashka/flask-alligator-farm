from xml.dom import NotFoundErr
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for
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

@app.route("/alligators/new", methods=["GET", "POST"])
def create_alligator():
    if request.method == "GET":
        return render_template("create_alligator.html")
    elif request.method == "POST":
        try:
            name = request.form.get("name-input")
            age = request.form.get("age-input")
            print("aargh", name, age)
            result = Alligator.create(name, age)

            return redirect(url_for("interact_with_alligator", id=result.id))
            
        except Exception as err:
            print(err)
            raise exceptions.BadRequest

@app.errorhandler(exceptions.NotFound)
def page_not_found(err):
    return render_template("404.html", error=err)

@app.errorhandler(exceptions.BadRequest)
def bad_request(err):
    return render_template("400.html", error=err)

if __name__ == "__main__":
    app.run(debug=True)