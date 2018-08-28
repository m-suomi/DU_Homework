# basic flask app to render stuff
from flask import Flask, render_template, redirect
from flask import jsonify
from flask import request

app = Flask(__name__)

#connect to mars database from mongo
from flask_pymongo import PyMongo #get PyMongo module to manage the MongoDB connection
app.config['MONGO_URI'] = 'mongodb://localhost:27017/mars'
mongo = PyMongo(app)


@app.route('/', methods=['GET'])
def index_latest_mars_data():
  collection = mongo.db.mars_data
  #get most recent scrape data (_id is saved as timestamp in my scrape/to_mongo scripts)
  #so sort that _id by descending (-1) and take first one
  latest_mars_data = collection.find_one(sort = [('_id', -1)])
  return render_template('index.html', mars_data=latest_mars_data)


@app.route('/scrape')
def scrape_to_mongo():
  #import the functions from my python script
  from scrape_mars_to_mongo import scrape, to_mongo
  #run the scrape function 
  latest_scrape = scrape()
  #send data to mongo database
  to_mongo(latest_scrape)
  #redirect back to the index page to reload with the current data 
  return redirect('/', code=302)


app.run(debug=True, port=5545)