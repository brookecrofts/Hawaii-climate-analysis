import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
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
def welcome():
    """List all available api routes."""
    return (
        f"Welcome to your Hawaii Tourist Info!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0<start><br/>"
        f"/api/v1.0<<start>/<end>"
    )

@app.route("/api/v1.0/precipitation/<precipitation>")
def precipitation(precipitation):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of dates with prcp as key value pair"""
    # Query all dates
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_prcp
    all_prcp = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)


@app.route("/api/v1.0/stations/<stations>")
def stations(stations):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list all stations with name as key value pair"""
    # Query all dates
    results = session.query(Station.station, Station.name).all()

    session.close()

#     # Create a dictionary from the row data and append to a list of all_prcp
#     all_names = []
#     for station, name in results:
#         name_dict = {}
#         name_dict["station"] = station
#         name_dict["name"] = name
#         all_names.append(name_dict)
 
    ## OR JUST RETURN LIST RESULTS FROM ABOVE QUERY, DEPENDING ON HOW TO USE INFO LATER

    return jsonify(results)


@app.route("/api/v1.0/tobs/<tobs>")
def tobs(tobs):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all dates and temp observ of most active station for the last year of data"""
   
    most_recent_yr = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    most_recent_yr = dt.date(2017,8,23)
    year_ago = most_recent_yr - dt.timedelta(days=365)
    year = session.query(Measurement.station, Measurement.date, Measurement.prcp, Measurement.tobs).\
        filter(Measurement.station=='USC00519281', Measurement.date >=year_ago).all()

    session.close()

    # Convert list of tuples into normal list
    all_tobs = list(np.ravel(year))

    return jsonify(all_tobs)

# @app.route("/api/v1.0/<start>")
# def start(start):
#     # Create our session (link) from Python to the DB
#     session = Session(engine)

#     """Return a list of all passenger names"""
#     # Query all passengers
#     results = session.query(Hawaii.name).all()

#     session.close()

#     # Convert list of tuples into normal list
#     all_names = list(np.ravel(results))

#     return jsonify(all_names)

# @app.route("/api/v1.0/<start>/<end>")
# def startend(startend):
#     # Create our session (link) from Python to the DB
#     session = Session(engine)

#     """Return a list of all passenger names"""
#     # Query all passengers
#     results = session.query(Hawaii.name).all()

#     session.close()

#     # Convert list of tuples into normal list
#     all_names = list(np.ravel(results))

#     return jsonify(all_names)


if __name__ == '__main__':
    app.run(debug=True)
