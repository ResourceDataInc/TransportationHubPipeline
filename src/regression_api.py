"""
Deploys a model via API, allowing users to submit inputs and receive predictions.

- jrgarrar
"""

# SETUP #######################################################################
# Import libraries.
import os
import pickle
import numpy as np
from flask import Flask, request

# Set globals.
PARENTDIR = os.path.dirname(os.path.realpath(__file__))
MODELDIR = os.path.join(PARENTDIR, "../models")
MODEL = "linear_regression.pickle"


# HELPERS #####################################################################
def unpickle_model(filename):
    model_file = os.path.join(MODELDIR, filename)
    with open(model_file, "rb") as f:
        model = pickle.load(f)
    return model


def input_converter(json):
    sorted_json = [json[x] for x in sorted(json)]
    output = np.array(sorted_json).reshape(-1, 1).T
    return output


# MAIN ########################################################################
def create_app(test_config=None):
    app = Flask("regression_api", instance_relative_config=True)

    @app.route("/api/v1/predict", methods=["POST"])
    def get_predict():
        # Process input JSON.
        # For example, {"TIMESTAMP": 1717372220}
        inputs = input_converter(request.json)
        if inputs is None:
            return {"predict": -1}

        # Unpickle the model
        model = unpickle_model(MODEL)

        # Run prediction using the model.
        prediction = model.predict(inputs)

        # Return prediction.
        return {"predict": prediction[0]}

    return app
