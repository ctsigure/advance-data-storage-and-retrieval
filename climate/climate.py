import pandas as pd
import numpy as np
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

engine = create_engine("sqlite:///Resources/hawaii.sqlite",connect_args={'check_same_thread': False})
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start/<start><br/>"
        f"/api/v1.0/start_end/<start>/<end><br/>")


@app.route("/api/v1.0/precipitation")
def prcps():
    # Query all passengers
    prcp_results = session.query(Measurement.date, Measurement.prcp).all()
    prcp_dict = {}
    for prcp in prcp_results:
        dates = prcp.date
        precipitations = prcp.prcp
        prcp_dict.update({dates : precipitations})
    return jsonify(prcp_dict)

@app.route("/api/v1.0/stations")
def stations():
    station_results = session.query(Station.station).all()
    all_stations = list(np.ravel(station_results))
    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    tob_results = session.query(Measurement.tobs).filter(Measurement.date >= 2017-8-23).all()
    all_tobs = list(np.ravel(tob_results))
    return jsonify(all_tobs)


@app.route("/api/v1.0/start/<start>")
def start(start):
    results = pd.DataFrame(session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= start).all())
    return jsonify(
       {'min temp': results['tobs'].min(), 'ave temp': results['tobs'].mean(), 'max temp': results['tobs'].max()})

@app.route("/api/v1.0/start_end/<start>/<end>")
def start_end(start,end):
    combine_results = pd.DataFrame(session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= start).filter(Measurement.date <= end).all())
    return jsonify({'min temp': combine_results['tobs'].min(), 'ave temp': combine_results['tobs'].mean(), 'max temp': combine_results['tobs'].max()})

if __name__ == '__main__':
    app.run(debug=True)

