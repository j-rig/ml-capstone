from socket import gethostname
from uuid import uuid4
import datetime
import json
import os
import locale
import hashlib

from flask_wtf import FlaskForm as Form
from wtforms import StringField, SubmitField
from wtforms import validators, TextAreaField
from wtforms.fields import EmailField
from flask import session, redirect, request, jsonify
from flask import Flask, Response
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_basicauth import BasicAuth
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_restful import Resource, Api
from werkzeug.exceptions import HTTPException
from flask_bootstrap import Bootstrap


from bizwiz.pipeline import pipeline, predict_funcs, listing_funcs

locale.setlocale(locale.LC_ALL, "en_US.UTF-8")

app = Flask(__name__)

app.secret_key = os.environ.get("WEBAPP_SECRET", "word")

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "WEBAPP_DBURI", "sqlite:////tmp/bizwiz.sqlite"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["BASIC_AUTH_USERNAME"] = os.environ.get("WEBAPP_ADMIN_USER", "admin")
app.config["BASIC_AUTH_PASSWORD"] = os.environ.get("WEBAPP_ADMIN_PASS", "admin")
app.config["FLASK_ADMIN_SWATCH"] = "slate"

Bootstrap(app)
api = Api(app)
db = SQLAlchemy(app)
basic_auth = BasicAuth(app)
admin = Admin(app, name="bizwiz admin", template_mode="bootstrap3")


# Create models
class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String())
    ts = db.Column(db.DateTime)
    uuid = db.Column(db.String())
    url = db.Column(db.String())
    hurl = db.Column(db.String())
    visible = db.Column(db.Boolean)
    json = db.Column(db.String())


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String())
    ts = db.Column(db.DateTime)
    uuid = db.Column(db.String())
    email = db.Column(db.String())
    message = db.Column(db.String())


class Url(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String())
    ts = db.Column(db.DateTime)


# Create forms


class ContactForm(Form):
    email = EmailField("email", [validators.DataRequired(), validators.Email()])
    message = TextAreaField(
        "message", [validators.DataRequired(), validators.Length(min=6, max=2000)]
    )
    submit_button = SubmitField("submit")


base_url = "https://www.bizbuysell.com/Business-Opportunity"


def bbs_url_validator(form, field):
    url = field.data
    if not url.lower().startswith(base_url.lower()):
        raise validators.ValidationError(f"Url must begin with {base_url}")


class BizBuySellUrlForm(Form):
    url = StringField(
        "bizbuysell url",
        [
            validators.DataRequired(),
            bbs_url_validator,
            validators.Length(min=len(base_url) + 1, max=2083),
            validators.URL(),
        ],
    )
    submit_button = SubmitField("submit")


# basic auth for admin
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
admin.add_view(AuthModelView(Contact, db.session))
admin.add_view(AuthModelView(Url, db.session))


def as_dollar(n):
    return locale.currency(n, grouping=True)


def check_uuid():
    if "uuid" not in session:
        session["uuid"] = str(uuid4())


@app.route("/")
def home():
    check_uuid()
    return render_template("index.html")


@app.route("/blog")
def blog():
    check_uuid()
    return render_template("blog.html")


@app.route("/detail/<page_id>")
def detail(page_id):
    pl = (
        Prediction.query.filter_by(uuid=session["uuid"], visible=True, hurl=page_id)
        .limit(1)
        .all()
    )
    p = [json.loads(p.json) for p in pl][0]
    return render_template("detail.html", p=p, as_dollar=as_dollar)


@app.route("/dash", methods=["GET", "POST"])
def dash():
    check_uuid()
    # listings = []
    # if "listings" not in session:
    #     o = pipeline(dict(), listing_funcs)
    #     if "error" not in o.keys():
    #         session["listings"] = o["listings"]
    # else:
    #     listings = session["listings"]
    listings = Url.query.distinct(Url.url).order_by(Url.id.desc()).limit(100).all()
    js_listings = [f"'{x.url}'" for x in listings]
    js_listings = ",\n".join(js_listings)
    js_listings = f"listings=[{js_listings}];"
    form = BizBuySellUrlForm()
    if form.validate_on_submit():
        pred = Prediction()
        pred.ts = datetime.datetime.utcnow()
        pred.ip = request.remote_addr
        pred.uuid = session["uuid"]
        pred.url = form.url.data
        h = hashlib.new("sha256")
        h.update(form.url.data.encode())
        pred.hurl = h.hexdigest()
        pred.visible = True
        result = pipeline(dict(url=pred.url, hurl=pred.hurl), predict_funcs)
        del result["scratch"]
        pred.json = json.dumps(result)
        db.session.add(pred)
        db.session.commit()
        return redirect("/dash")
    pl = (
        Prediction.query.filter_by(uuid=session["uuid"], visible=True)
        .order_by(Prediction.id.desc())
        .limit(50)
        .all()
    )
    pll = [json.loads(p.json) for p in pl]
    return render_template(
        "dash.html", form=form, pl=pll, as_dollar=as_dollar, listings=js_listings
    )


# TODO
# @app.route("/export")
# @basic_auth.required
# def export():
#     check_uuid()
#     def generate():
#         pl = (
#             Prediction.query.filter_by(uuid=session["uuid"], visible=True)
#             .order_by(Prediction.id.desc())
#             .all()
#         )
#         pll = [json.loads(p.json) for p in pl]
#         #print(pll)
#         yield f'id,url,price,model_price\n'
#         for p in pll:
#             if 'error' not in p.keys():
#                 yield f'{p.id},{p.url},{p.price},{p.pprice}\n'
#     return Response(generate(), mimetype='text/csv')


@app.route("/about")
def about():
    check_uuid()
    return render_template("about.html")


@app.route("/env")
@basic_auth.required
def env():
    def generate():
        for k, v in os.environ.items():
            yield f"{k}={v}\n"

    return Response(generate(), mimetype="text/plain")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    check_uuid()
    form = ContactForm()
    if form.validate_on_submit():
        contact = Contact()
        contact.ts = datetime.datetime.utcnow()
        contact.ip = request.remote_addr
        contact.uuid = session["uuid"]
        contact.email = form.email.data
        contact.message = form.message.data
        db.session.add(contact)
        db.session.commit()
        return redirect("/contact/thanks")
    return render_template("contact.html", form=form)


@app.route("/contact/thanks")
def thanks():
    check_uuid()
    return render_template("thanks.html")


class bizBuySellUrl(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        result = pipeline(json_data, predict_funcs)
        del result["scratch"]
        return jsonify(result)


api.add_resource(bizBuySellUrl, "/api/bizbuysell/url")


class bizBuySellListings(Resource):
    def get(self):
        listings = []
        ts = datetime.datetime.utcnow()
        o = pipeline(dict(), listing_funcs)
        if "error" not in o.keys():
            listings = o["listings"]
        for l in listings:
            u = Url()
            u.url = l
            u.ts = ts
            db.session.add(u)
        db.session.commit()
        return jsonify(listings)


api.add_resource(bizBuySellListings, "/api/bizbuysell/listings")

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    if "liveconsole" not in gethostname():
        app.run(debug=True, host="0.0.0.0")
