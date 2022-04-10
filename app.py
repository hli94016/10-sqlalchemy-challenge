import numpy as np
import pandas as pd
import datetime as dt
from pandas.plotting import table

from flask import Flask, jsonify

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
measurementTable = Base.classes.measurement
stationTable = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

app = Flask(__name__)

@app.route("/")
def indexRoute():
    routes = ['/', '/api/v1.0/precipitation', '/api/v1.0/stations', '/api/v1.0/tobs', '/api/v1.0/<start>', '/api/v1.0/<start>/<end>']
    return jsonify(routes = routes)

@app.route("/api/v1.0/precipitation")
def getPrecipitation():
    # Calculate the date one year from the last date in data set.
    timeDiff = dt.date(2017,8,23) - dt.timedelta(days = 365)

    # Perform a query to retrieve the data and precipitation scores
    datas = session.query(measurementTable.date, measurementTable.prcp).filter(measurementTable.date >= timeDiff).all()

    session.close()

    resDict = {}
    print(datas)
    for data in datas:
        date = data[0]
        precipitation = data[1]
        resDict[date] = precipitation
    return jsonify(resDict)

@app.route("/api/v1.0/stations")
def getStations():
    datas = session.query(stationTable.station).all()
    session.close()

    res = []
    for data in datas:
        res.append(data[0])
    return jsonify(res = res)

@app.route("/api/v1.0/tobs")
def getTobs():
    # Calculate the date one year from the last date in data set.
    timeDiff = dt.date(2017,8,23) - dt.timedelta(days = 365)

    # Using the most active station id
    # Query the last 12 months of temperature observation data for this station and plot the results as a histogram

    lastYearTempObservation = session.query(measurementTable.tobs).filter(measurementTable.date >= timeDiff).filter(measurementTable.station == 'USC00519281').all()

    session.close()

    res = []
    for data in lastYearTempObservation:
        res.append(data[0])
    return jsonify(res = res)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def getMinAvgMaxTemperatureList(start = None, end = None):

    if end is None:
        start = dt.datetime.strptime(start, "%m%d%Y")
        datas = session.query(func.min(measurementTable.tobs), func.max(measurementTable.tobs), func.avg(measurementTable.tobs)).filter(measurementTable.date >= start).all()
        session.close()
        res = []
        for data in datas:
            res.append(data[0])
        return jsonify(res = res)
    else:
        start = dt.datetime.strptime(start, "%m%d%Y")
        end = dt.datetime.strptime(end, "%m%d%Y")

        datas = session.query(func.min(measurementTable.tobs), func.max(measurementTable.tobs), func.avg(measurementTable.tobs)).filter(measurementTable.date >= start).filter(measurementTable.date <= end).all()
        session.close()

        res = []
        for data in datas:
            res.append(data[0])
        return jsonify(res = res)

if __name__ == '__main__':
	app.run(debug=True)