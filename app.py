import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)


Measurement = Base.classes.measurement

Station = Base.classes.station

app = Flask(__name__)

session = Session(engine)


@app.route("/")
def welcome():
    return (
    f"Available Routes:<br/>"
    f"Total Precipitation URL: /api/v1.0/precipitation<br/>"        
    f"List of active stations URL: /api/v1.0/stations<br/>"
    f"Temperature Readings from past year at station USC00519281 URL: /api/v1.0/tobs<br/>"
    f"Max, Min, and Avg Temperature Readings given start date or start and end date URL: /api/v1.0/<start> or /api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()
    all_prcp = []
    for date, prcp, in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    session.close()
    all_stations = list(np.ravel(results))
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    results = session.query(Measurement.station, Measurement.date, Measurement.tobs).filter(Measurement.date >= '2016-08-01').filter(Measurement.station == 'USC00519281').all()
    session.close()
    USC00519281temp = list(np.ravel(results))
    return jsonify(USC00519281temp)

@app.route("/api/v1.0/<start>/<end>")
def range(start, end):
    
    sel = [func.max(Measurement.tobs), 
        func.min(Measurement.tobs),
        func.avg(Measurement.tobs)]

    results = session.query(*sel).filter(Measurement.date > start).filter(Measurement.date < end).all()
    
    session.close()

    tempbetweendates = list(np.ravel(results))
    return jsonify(tempbetweendates)

@app.route("/api/v1.0/<start>")
def startdate(start):
    sel = [func.max(Measurement.tobs), 
        func.min(Measurement.tobs),
        func.avg(Measurement.tobs)]

    results = session.query(*sel).filter(Measurement.date >= start).all()

    session.close()

    begindatetemp = list(np.ravel(results))
    return jsonify(begindatetemp)


if __name__ == '__main__':
    app.run(debug=True)