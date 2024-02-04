# Import the dependencies.
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from datetime import datetime, timedelta
from sqlalchemy.orm import scoped_session, sessionmaker
#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///C:\\Users\\Banni\\Desktop\\Class Files\\sqlalchemy-challenge\\Starter_Code\\Resources\\hawaii.sqlite")


# reflect an existing database into a new model
Base=automap_base()


# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)

start_date = '2010-01-03'
end_date = '2010-02-15'

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///C:\\Users\\Banni\\Desktop\\Class Files\\sqlalchemy-challenge\\Starter_Code\\Resources\\hawaii.sqlite"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

engine = create_engine("sqlite:///C:\\Users\\Banni\\Desktop\\Class Files\\sqlalchemy-challenge\\Starter_Code\\Resources\\hawaii.sqlite")
session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date/{start_date}<br/>"
        f"/api/v1.0/start_date_end_date/{start_date}/{end_date}"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    precipitation_data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    precipitation_dict = {date: prcp for date, prcp in precipitation_data}
    return jsonify(precipitation_dict)

@app.route("/api/v1.0/stations")
def stations():
    stations = session.query(Station.station, Station.name).all()
    station_dict = {station: name for station, name in stations}
    return jsonify(station_dict)

@app.route("/api/v1.0/tobs")
def tobs():
    
    most_active_stations = session.query(Measurement.station, func.count(Measurement.station)).\
        group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()
    most_active_station_id = most_active_stations[0][0]

    tobs_data = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == most_active_station_id).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    tobs_dict = {date: tobs for date, tobs in tobs_data}
    return jsonify(tobs_dict)

@app.route(f"/api/v1.0/start_date/{start_date}")
def temperature_start_date():
    temperature_start_data = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.station == most_active_station_id).\
        filter(Measurement.date >= start_date).all()

    temperature_start_dict = {
        "Minimum Temperature": temperature_start_data[0][0],
        "Maximum Temperature": temperature_start_data[0][1],
        "Average Temperature": temperature_start_data[0][2]
    }

    return jsonify(temperature_start_dict)

@app.route(f"/api/v1.0/start_date_end_date/{start_date}/{end_date}")
def temperature_date_range():
    temperature_range_data = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.station == most_active_station_id).\
        filter(Measurement.date >= start_date).\
        filter(Measurement.date <= end_date).all()

    temperature_range_dict = {
        "Minimum Temperature": temperature_range_data[0][0],
        "Maximum Temperature": temperature_range_data[0][1],
        "Average Temperature": temperature_range_data[0][2]
    }

    return jsonify(temperature_range_dict)

if __name__ == '__main__':
    app.run(debug=True)