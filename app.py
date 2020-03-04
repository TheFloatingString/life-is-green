from flask import Flask, request, render_template, redirect, url_for, jsonify
from flask_cors import CORS, cross_origin
from db.models import Entry
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json
import os

# Postgres
engine = create_engine(os.environ["DATABASE_URL"], echo = 'debug')

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

# Flask
app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

@app.route("/")
@cross_origin()
def home():
	return render_template("home.html")

@app.route("/get_entries", methods=["GET"])
@cross_origin()
def get_entries():
	return_dict = dict()
	return_dict["data"] = list()
	for entry in session.query(Entry):
		return_dict["data"].append(entry.message)
	return jsonify(return_dict)

@app.route("/create_entry_form")
@cross_origin()
def create_entry_form():
	return render_template("form.html")

@app.route("/create_entry", methods=["GET", "POST"])
@cross_origin()
def create_entry():
	print(request.form)
	if request.method=="POST" and (request.form["message"] is not None):
		entry = Entry()
		entry.create_entry(request.form["message"])
		session.add(entry)
		session.commit()
		return redirect(url_for("/"))

@app.route("/success")
def success():
	return render_template("success.html")

if __name__ == '__main__':
	app.run(debug=True, port=5000, host="0.0.0.0")
