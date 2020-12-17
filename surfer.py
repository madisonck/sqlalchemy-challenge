#import dependencies
import numpy as np
import datetime as dt

#import flask
from flask import Flask, jsonify

#import python SQL and ORM
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#create connection sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

#reflect db into model
Base = automap_base()

#reflect tables
Base.prepare(engine, reflect=True)

#save references
Measurement = Base.classes.measurement
Station = Base.classes.station

#create link to session
session = Session(engine)

#setup flask
app = Flask(__name__)

#flask routes

@app.route("/")
def welcome():
	return ("Available Routes on this API Server<br/>"
		f"/api/v1.0/precipitation<br/>"
		f"/api/v1.0/Station<br/>"
		f"/api/v1.0/tobs<br/>"
		f"/api/v1.0/(Y-M-D)<br/>"
		f"/api/v1.0(start=Y-M-D)/(end=Y-M-D)<br/>"
	)

@app.route("/api/v1.0/precipitation")
def precipitation():
	results = session.query(Measurement).all()
	session.close()
	PrecipYear = []
	for result in results:
		PrecipYearDict = {}
		PrecipYearDict["date"] = result.date
		PrecipYearDict["prcp"] = result.prcp
		PrecipYear.append(PrecipYearDict)
	return jsonify(PrecipYear)

@app.route("/api/v1.0/Station")
def stations():
	StationData = session.query(Station.station).all()
	session.close()
	StationList = list(np.ravel(StationData))
	return jsonify(StationList)

@app.route("/api/v1.0/tobs")
def observations():
	OneYear = dt.date(2017, 8, 23) - dt.timedelta(days=365)
	OneYearObs = session.query(Measurement.tobs).filter(Measurement.date > OneYear).all()
	session.close()
	OneYearObsData = list(np.ravel(OneYearObs))
	return jsonify(OneYearObsData)

@app.route("/api/v1.0/<start>")
def DateStart(start):
	DateFirst = dt.datetime.strptime(start,"%Y-%m-%d")
	StatsInfo = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.round(func.avg(Measurement.tobs))).\
	filter(Measurement.date >= DateFirst).all()
	session.close() 
	StatsData = list(np.ravel(StatsInfo))
	return jsonify(StatsData)

@app.route("/api/v1.0/<start>/<end>")
def DatesBoth(start,end):
	DateFirst = dt.datetime.strptime(start,"%Y-%m-%d")
	DateLast = dt.datetime.strptime(end,"%Y-%m-%d")
	StatsInfo = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.round(func.avg(Measurement.tobs))).\
	filter(Measurement.date.between(DateFirst,DateLast)).all()
	session.close()    
	StatsData = list(np.ravel(StatsInfo))
	return jsonify(StatsData)

if __name__ == "__main__":
	app.run(debug=True)
