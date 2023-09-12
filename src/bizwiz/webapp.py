from socket import gethostname

from flask import Flask, Response
from flask_sqlalchemy import SQLAlchemy
from flask_basicauth import BasicAuth
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_restful import Resource, Api
from werkzeug.exceptions import HTTPException

app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/bizwiz.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["BASIC_AUTH_USERNAME"] = "admin"
app.config["BASIC_AUTH_PASSWORD"] = "admin"
app.config["FLASK_ADMIN_SWATCH"] = "cerulean"

api = Api(app)
db = SQLAlchemy(app)
basic_auth = BasicAuth(app)
admin = Admin(app, name="bizwiz admin", template_mode="bootstrap3")


# Create models
class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String())
    text = db.Column(db.String())
    model = db.Column(db.String())
    result = db.Column(db.String())


class AuthException(HTTPException):
    def __init__(self, message):
        super().__init__(
            message,
            Response(
                message, 401, {"WWW-Authenticate": 'Basic realm="Login Required"'}
            ),
        )


class AuthModelView(ModelView):
    def is_accessible(self):
        if not basic_auth.authenticate():
            raise AuthException("Not authenticated. Refresh the page.")
        else:
            return True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(basic_auth.challenge())


admin.add_view(AuthModelView(Prediction, db.session))


@app.route("/")
def hello():
    return "Hello, World!"


class HelloWorld(Resource):
    def get(self):
        return {"hello": "world"}


api.add_resource(HelloWorld, "/api/hello")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        if "liveconsole" not in gethostname():
            app.run(debug=True, host="0.0.0.0")
