from flask import Flask, redirect, url_for
from flask_dance.contrib.google import make_google_blueprint, google

import os

app = Flask(__name__)
app.secret_key = os.environ['FLASK_SECRET']

blueprint = make_google_blueprint(
    client_id=os.environ['GOOGLE_ID'],
    client_secret=os.environ['GOOGLE_SECRET'],
    scope=["profile", "email"]
)
app.register_blueprint(blueprint, url_prefix="/login")

@app.route("/")
def index():
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/plus/v1/people/me")
    assert resp.ok, resp.text
    return "You are {email} on Google".format(email=resp.json()["emails"][0]["value"])

if __name__ == "__main__":
    app.run(debug=True,)
