import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources\hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurement = Base.classes.measurement
station =  Base.classes.station

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
        f"Available Routes:<br/>"
        f"/home</br>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations</br>"
        f"/api/v1.0/tobs</br>"
        f"/api/v1.0/<start> and /api/v1.0/<end></br>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    query = session.query(measurement.date, measurement.prcp).filter(measurement.date >= date1).all()

    session.close()

    query_list = []
    
    for date, prcp in query:
        perc_dict = {}
        perc_dict['date'] = date
        perc_dict['prcp'] = prcp
        query_list.append(perc_dict)
    
    return jsonify(query_list)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    query = session.query(station.station, station.name, station.latitude, station.longitude, station.elevation).all()
    session.close()

    query_list = []
    for id, name, lat, long, e in query:
        station_dict = {}
        station_dict['id'] = id
        station_dict['name'] = name
        station_dict['Latitude'] = lat
        station_dict['Longitude'] = long
        station_dict['Elevation'] = e
        query_list.append(station_dict)
        
    return jsonify(query_list)


@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    query = session.query(measurement.date).order_by(desc(measurement.date)).first()
    recent_date_str = datetime.strptime(query[0], '%Y-%m-%d')
    date1 = dt.date(recent_date_str.year - 1, recent_date_str.month, recent_date_str.day)
    last12m_tobs = session.query(measurement.date, measurement.tobs).filter(measurement.date >= date1).all()

    query_list = []
    for date, tobs in last12m_tobs:
        tobs_dict = {}
        tobs_dict['date'] = date
        tobs_dict['tobs'] = tobs
        query_list.append(tobs_dict)

    return jsonify(tobs_dict)


@app.route("/api/v1.0/<start> and /api/v1.0/<end>")
def range(start, end):
    if start != None and end != None:
        query = session.query(measurement.station, func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs), func.count(measurement.tobs)).filter(measurement.date >= start).filter(measurement.date <= end).all()
    else:
        query = session.query(measurement.station, func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs), func.count(measurement.tobs)).filter(measurement.date >= start).all()

    query_list = []
    for station, min_tobs, max_tobs, avg_tobs in query:
        range_dict = {}
        range_dict['station'] = station
        range_ditct['min'] = min
        range_dict['max'] = max
        range_dict['avg'] = avg
        query_list.append(range_dict)
    
    return jsonify(range_dict)

if __name__ == '__main__':
    app.run(debug=True)
