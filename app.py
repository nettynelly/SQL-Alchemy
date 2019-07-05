
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine('sqlite:///hawaii.sqlite', echo=False)

# Declare a Base using `automap_base()`
Base = automap_base()

# Reflect Database into ORM classes
Base.prepare(engine, reflect=True)
Base.classes.keys()
# Save a reference to the measurenment table as 'Measurement'
Measurement = Base.classes.measurement
# Save a reference to the station table as 'Station'
Station = Base.classes.stations

# Create our session (link) from Python to the DB
session = Session(engine)

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
        "Hawaii Precipitation and Weather Data<br/><br/>"
        "Pick from the available routes below:<br/><br/>"
        "Precipiation from 2016-08-23 to 2017-08-23.<br/>"
        "/api/v1.0/precipitation<br/><br/>"
        "A list of all the weather stations in Hawaii.<br/>"
        "/api/v1.0/stations<br/><br/>"
        "The Temperature Observations (tobs) from 2016-08-23 to 2017-08-23.<br/>"
        "/api/v1.0/tobs<br/><br/>"
        "Type in a single date (i.e., 2015-01-01) to see the min, max and avg temperature since that date.<br/>"
        "/api/v1.0/temp/<start><br/><br/>"
        "Type in a date range (i.e., 2015-01-01/2015-01-10) to see the min, max and avg temperature for that range.<br/>"
        "/api/v1.0/temp/<start>/<end><br/>"
    )

days_12months_past = dt.date(2017,8,23) - dt.timedelta(days=365)
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Query for the dates and temperature observations from the last year.
    Convert the query results to a Dictionary using date as the 'key 'and 'tobs' as the value."""


    # Retrieve the last 12 months of precipitation data
    precipitation_scores = session.query(Measurement.date, 
    Measurement.prcp).filter(Measurement.date >= days_12months_past).all()

    # Create a dictionary from the row data and append to a list of for the precipitation data
    precipitation_data = []
    for prcp_data in precipitation_scores:
        prcp_data_dict = {}
        prcp_data_dict["Date"] = prcp_data_dict.date
        prcp_data_dict["Precipitation"] = prcp_data_dict.prcp
        precipitation_data.append(prcp_data_dict)
        

    return jsonify(precipitation_data)


@app.route("/api/v1.0/stations")
def stations():
    """Return a json list of stations from the dataset."""
    # Query all the stations
    number_of_stations = session.query(Measurement.station).distinct().count()

    # Create a dictionary from the row data and append to a list of all_stations.
    all_stations = []
    for stations in number_of_stations:
        stations_dict = {}
        stations_dict["Station"] = stations.station
        stations_dict["Station Name"] = stations.name
        stations_dict["Latitude"] = stations.latitude
        stations_dict["Longitude"] = stations.longitude
        stations_dict["Elevation"] = stations.elevation
        all_stations.append(stations_dict)
    
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return a json list of Temperature Observations (tobs) for the previous year"""
    # Query all the stations and for the given date. 
    temps_records = session.query(Measurement.station, Measurement.date, Measurement.tobs).\
    filter(Measurement.station == top_most_active_station).\
    filter(Measurement.date > days_12months_past).\
    order_by(Measurement.date).all()
                    
    # # Create a list of dicts with `date` and `tobs` as the keys and values
    temp_data = []
    for tobs_data in temps_records:
        tobs_data_dict = {}
        tobs_data_dict["Station"] = temps_records [0]
        tobs_data_dict["Date"] = temps_records [1]
        tobs_data_dict["tobs"] = temps_records [2]
        temp_data.append(tobs_data_dict)
    
    return jsonify(temp_data)
    

    
    return jsonify(begin_end_stats)

if __name__ == '__main__':
    app.run(debug=True)