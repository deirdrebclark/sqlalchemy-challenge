import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify, request

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the tables
Station = Base.classes.station
Measurement = Base.classes.measurement

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )
@app.route("/api/v1.0/precipitation")
def names():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of precipitation by date"""
    # Query 
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    # Create a dictionary and return all dates with precipitation
    all_dates = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict[date] = prcp
        all_dates.append(prcp_dict)
    
    return jsonify(all_dates)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of stations"""
    # Query 
    results = session.query(Station.station).all()

    session.close()

    # Create a dictionary and return all stations
    all_stations = []
    for station in results:
        station_dict = {}
        station_dict[station] = station
        all_stations.append(station_dict)
    
    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of temperature observations """
    # Queries
    end_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    start_date = dt.date(end_date) - dt.timedelta(days = 365)

    results = session.query(Measurement.date, Measurement.tobs).\
        filter(func.strftime(Measurement.date) >= start_date).all()

    session.close()

    # Create a dictionary and return all stations
    all_tobs = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict[date] = tobs
        all_tobs.append(tobs_dict)
    
    return jsonify(all_tobs)


@app.route("/api/v1.0/<start>")
def tobs_by_start_date():
    # Create session from Python to the DB
    session = Session(engine)

    """Return a list of temperatures greater than the start date"""
    # Pull in requested start date
    start_date = request.args.get('start')

    # Query
    results = session.query(Measuerement.date,\
        func.min(Measurement.tobs.label("TMIN")),\
            func.avg(Measurement.tobs.label("TAVG")),\
                func.max(Measurement.tobs.label("TMAX"))).\
                    filter(func.strftime(Measurement.date) >= start_date).all()
    
    # Create a dictionary and return TMIN, TAVG, and TMAX from the start date
    all_tobs = []
    for date, TMIN, TAVG, TMAX in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["TMIN"] = TMIN
        tobs_dict["TAVG"] = TAVG
        tbox_dict["TMAX"] = TMAX
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)


@app.route("/api/v1.0/<start>/<end>")
def tobs_by_start_date():
    # Create session from Python to the DB
    session = Session(engine)

    """Return a list of temperatures greater than the start date"""
    # Pull in requested start date
    start_date = request.args.get("start")
    end_date = request.args.get("end")

    # Query
    results = session.query(Measuerement.date,\
        func.min(Measurement.tobs.label("TMIN")),\
            func.avg(Measurement.tobs.label("TAVG")),\
                func.max(Measurement.tobs.label("TMAX"))).\
                    filter(func.strftime(Measurement.date) >= start_date).\
                        filter(Measurement.date <= end_date).all()
    
    # Create a dictionary and return TMIN, TAVG, and TMAX from the start date
    all_tobs = []
    for date, TMIN, TAVG, TMAX in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["TMIN"] = TMIN
        tobs_dict["TAVG"] = TAVG
        tbox_dict["TMAX"] = TMAX
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)


if __name__ == '__main__':
    app.run(debug=True)   


