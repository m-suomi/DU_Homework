#run this code in your anaconda prompt "python climate_app_flask.py"
#go to the base web address it tells you its running at

from flask import Flask, jsonify, render_template
import json
import requests
from flask import request
import pandas as pd
import numpy as np
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func
from sqlalchemy.ext.automap import automap_base
from datetime import datetime, timedelta

#flask setup
app = Flask(__name__)

#set up the SQL Alchemy engine connection to the database
engine = create_engine('sqlite:///raw_data/hawaii.sqlite?check_same_thread=False')
Base = automap_base()
Base.prepare(engine, reflect=True)
session = Session(bind=engine)

Measurement = Base.classes.hawaii_measurements
Station = Base.classes.hawaii_stations

#provide home page with some basic summary info about the API
@app.route('/')
def home_route():
    return """
            <body>
                <div class="container">
                    <h1>Welcome to the Climate App data for Hawaii - use the following APIs:</h1>
                    <p>Dates and Average Precipitation Observations from the last year of data:  /api/v1.0/precipitation</p>
                    <p>List of Stations in the Dataset:  /api/v1.0/stations </p>
                    <p>Temperature Observations (tobs) for the previous year of data:  /api/v1.0/tobs  </p>
                    <p>Min, Avg, Max Temps for Given Start Date:  /api/v1.0/start </p>
                    <p>Min, Avg, Max Temps for Given Start-End Date Range:  /api/v1.0/start/end </p>
                </div>
            </body>
            """


# Query for the dates and average precipitation observations from the last year.
# Convert the query results to a Dictionary using date as the key and precip
# as the value.
# Return the JSON representation of your dictionary.
@app.route('/api/v1.0/precipitation')
def last_12_month_precip():
    #find the max date in the data and then find 12 months ago date to get year of data
    last_precip_date = max(session.query(Measurement.datetime))[0]
    year_ago_precip_date = last_precip_date - timedelta(days=365)
    #retrieve the last 12 months of data - average it by date so includes all of the station info --
    #if didn't average it, would only return one stations worth of data because can only have one key in a
    # dictionary and date is being used as the key and multiples of each date in the dataset
    #query the date text values instead of datetime values for easier conversion to json
    last_12_months_prcp = session.query(Measurement.date, func.avg(Measurement.prcp).label('precipitation'))\
                        .filter(Measurement.datetime > year_ago_precip_date)\
                        .group_by(Measurement.date)
    df_prcp_last_12_months = pd.read_sql(last_12_months_prcp.statement, session.bind, index_col='date')
    #put data into dictionary
    #df_precip_last_12_months.sort_index(inplace=True) #no need to sort because putting into a dictionary
    dict_prcp = df_prcp_last_12_months.to_dict().get('precipitation')

    
    return jsonify({'keys_label': 'date', 'values_label': 'average_precipitation',
                     'prcp_data_last_12_months':dict_prcp})
   

#return a JSON list of stations from the dataset.
@app.route('/api/v1.0/stations')
def stations():
    stations = session.query(Station.name).all()
    #unpack the list of tuples that is returned
    stations_list = [x[0] for x in stations]

    return jsonify({'stations_names': stations_list})


#Return a JSON list of Temperature Observations (tobs) for the previous year
#this seems kind of silly to return the values without an associate date, but do what HW wants...
@app.route('/api/v1.0/tobs')
def last_12_month_temp():
    #find the max date in the data and then find 12 months ago date to get year of data
    last_tobs_date = max(session.query(Measurement.datetime))[0]
    year_ago_tobs_date = last_tobs_date - timedelta(days=365)
    #retrieve the last 12 months of tobs data only
    last_12_months_tobs = session.query(Measurement.tobs)\
                        .filter(Measurement.datetime > year_ago_tobs_date).all()
    #unpack the list of tuples that is returned
    last_12_months_tobs_list = [x[0] for x in last_12_months_tobs]
    return jsonify({'tobs_data_last_12_months': last_12_months_tobs_list})


#Return a JSON list of the minimum temperature, the average temperature, and the max temperature for
# a given start date.
#When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
#input is date in form of %Y-%m-%d
@app.route('/api/v1.0/<start>')
def calc_temps_start(start):
    start_date_dt = datetime.strptime(start, '%Y-%m-%d').date()
    #provide end date of data
    end_date_dt = max(session.query(Measurement.datetime))[0]
    end_date = datetime.strftime(end_date_dt, '%Y-%m-%d')

    temp_data_min_max_avg = session.query(func.min(Measurement.tobs),
                                         func.max(Measurement.tobs),
                                         func.avg(Measurement.tobs))\
                                .filter(Measurement.datetime >= start_date_dt)\
                                .all()
    temp_min = temp_data_min_max_avg[0][0] 
    temp_max = temp_data_min_max_avg[0][1]
    temp_avg = temp_data_min_max_avg[0][2]
    
    return jsonify({'Start_Date': start, 'Last_Date_of_Dataset': end_date,
                     'TMIN': temp_min, 'TAVG': temp_avg, 'TMAX': temp_max}) 

#Return a JSON list of the minimum temperature, the average temperature, and the max temperature for
# a given start-end range.
#When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and
# end date inclusive.
@app.route('/api/v1.0/<start>/<end>')
def calc_temps(start, end):
    start_date_dt = datetime.strptime(start, '%Y-%m-%d').date()
    end_date_dt = datetime.strptime(end, '%Y-%m-%d').date()
                   
    temp_data_min_max_avg = session.query(func.min(Measurement.tobs),
                                         func.max(Measurement.tobs),
                                         func.avg(Measurement.tobs))\
                                .filter(Measurement.datetime >= start_date_dt)\
                                .filter(Measurement.datetime <= end_date_dt)\
                                .all()
    temp_min = temp_data_min_max_avg[0][0] 
    temp_max = temp_data_min_max_avg[0][1]
    temp_avg = temp_data_min_max_avg[0][2]
    
    #if dates are beyond end of data set, provide warning to api request
    last_date_dt = max(session.query(Measurement.datetime))[0]
    last_date = datetime.strftime(last_date_dt, '%Y-%m-%d')
    if start_date_dt > last_date_dt or end_date_dt > last_date_dt:
        return jsonify({'warning': f'Last Date of Dataset is {last_date} - choose dates within dataset'}) 
    else:
        return jsonify({'Start_Date': start, 'End_Date': end, 'TMIN': temp_min, 'TAVG': temp_avg, 'TMAX': temp_max}) 


#flask debugging setup
if (__name__ == "__main__"): 
    app.run(port = 5545, debug=True)