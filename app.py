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
        f"/api/v1.0/<start> and /api/v1.0/<start>/<end></br>"
    )


@app.route("/api/v1.0/precipitation")
def names():
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

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)


@app.route("/api/v1.0/stations")
def passengers():
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



    # Create a dictionary from the row data and append to a list of all_passengers
    all_passengers = []
    for name, age, sex in results:
        passenger_dict = {}
        passenger_dict["name"] = name
        passenger_dict["age"] = age
        passenger_dict["sex"] = sex
        all_passengers.append(passenger_dict)

    return jsonify(all_passengers)


if __name__ == '__main__':
    app.run(debug=True)
