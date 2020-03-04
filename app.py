from flask import Flask, request, render_template, redirect, url_for
from db.models import Entry
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json

# Postgres
engine = create_engine(os.environ["DATABASE_URL"], echo = 'debug')

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

# Flask
app = Flask(__name__)

@app.route("/")
def home():
	return render_template("home.html")

@app.route("/get_entries", methods=["GET"])
def get_entries():
	return_dict = dict()
	return_dict["data"] = list()
	for entry in session.query(Entry):
		return_dict["data"].append(entry.message)
	return json.dumps(return_dict)

@app.route("/create_entry_form")
def create_entry_form():
	return render_template("create_entry_form.html")

@app.route("/create_entry", methods=["GET", "POST"])
def create_entry():
	if request.method=="POST" and (request.args.get("message") is not None):
		entry = Entry()
		entry.create_entry(request.args.get("message"))
		session.add(entry)
		session.commit()
		return home()
		
@app.route("/success")
def success():
	return render_template("success.html")

if __name__ == '__main__':
	app.run(debug=True, port=5000, host="0.0.0.0")
