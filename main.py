import os
import numpy as np
import json
import flask

from encoders import NpEncoder
from model.predict import predict

app = flask.Flask("model-test")

@app.route("/isAlive", methods=["GET"])
def is_alive():
    return "true"

@app.route("/predict", methods=["POST"])
def predict_route():
    result = predict( flask.request.json )

    response = flask.Response( json.dumps(result, cls=NpEncoder) )
    response.headers['content-type'] = 'application/json'
    
    return(response)

if __name__ == "__main__":
    if "ENVIROMENT" in os.environ and os.environ["ENVIROMENT"] == "PRODUCTION":
        app.run(port=80, host="0.0.0.0")
    else:
        app.run(port=8080, host="0.0.0.0")