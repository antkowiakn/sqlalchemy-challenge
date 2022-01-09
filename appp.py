#some of the lines below 2-30 used for guidance with setting up tasks from Ins_Flask_with_ORM Unit 10- Class 3-Lesson 10

import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, session
from sqlalchemy import create_engine, func, inspect
import datetime as dt
import numpy as np

from flask import Flask, jsonify

#Database Setup
engine = create_engine("sqlite:///hawaii.sqlite")

#reflect database to a model
Base= automap_base()
#reflect the tables
Base.prepare(engine, reflect=True)

#save the reference for the tables
measurement = Base.classes.measurement
station = Base.classes.station

#start flask setuo
app= Flask(__name__)
#routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return(
        f'Climate Homepage<br>'
        f'Routes:<br>'
        f'/api/v1.0/precipitation<br>'
        f'/api/v1.0/stations<br>'
        f'/api/v1.0/tobs<br>'
        f'/api/v1.0/<start><br>'
        f'/api/v1.0/<start>/<end><br>'
    )

@app.route('/api/v1.0/precipitation')
def prcp():
    session=Session(engine)
    #from one year of last data query and order the data by date
    oneyrdate = dt.date(2017,8,23) - dt.timedelta(days=365)
    scores = session.query(measurement.date, measurement.prcp).filter(measurement.date >= oneyrdate).order_by(measurement.date).all()
    scores_dict = dict(scores)
    session.close()
    return jsonify(scores_dict)

@app.route('/api/v1.0/stations')
def station():
    session=Session(engine)
    #query for all active stations in desc. order for each station and the count for each stations measurement
    active_stations = session.query(measurement.station, func.count()).group_by(measurement.station).order_by(func.count().desc())
    stations_dit = dict(active_stations)
    session.close()

    #create a list to hold all of the results
    active_station=[]
    for result in active_stations:
        station_dict ={}
        stations_dit["station"] = result[0]
        active_station.append(stations_dit)

    return jsonify(stations_dit)

@app.route('/api/v1.0/tobs')
def tobs():
    session=Session(engine)
    #query for the date and temp observation for the most active station which is station USC00519281
    observations = session.query(measurement.station, measurement.tobs).filter(measurement.date >='2016-08-23').filter(measurement.station == 'USC00519281').all()
    #create dictionary to keep results
    observation_station =[]
    for result in observations:
        most_active ={}
        most_active["date"] = result[0]
        most_active["tobs"] = result[1]
        observation_station.append(most_active)
    
    session.close()
    
    return jsonify(observation_station)

@app.route('/api/v1.0/<start>')
def start(start):
    session=Session(engine)
    #take the avg, min, max for measurement and filter by the date entered 
    start_date = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= start).all()
    session.close()
#create dictionary to keep results
    observation_all =[]
    for results in start_date:
        observation_dict ={}
        observation_dict["min"] = results[0]
        observation_dict["avg"] = results[1]
        observation_dict["max"] = results[2]
        observation_all.append(observation_dict)
   
    return jsonify(observation_dict)

@app.roure('/api/v1.0/<start>/<end>')
def srtend(start,end):
    session=Session(engine)
    #from the start date from above use the same and change carrot to close it so you can grab all days between dates requested
    end_date = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date <= end).all()
    session.close()
#use dictionary to keep results
    observation_all=[]
    for results in end_date:
        observation_dict ={}
        observation_dict["min"] = results[0]
        observation_dict["avg"] = results[1]
        observation_dict["max"] = results[2]
        observation_all.append(observation_dict)

    return jsonify(observation_dict)

if __name__ == '__main__':
    app.run(debug=True)