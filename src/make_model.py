"""
Generates a model using local data.

- jrgarrar
"""

# SETUP #######################################################################
# Import libraries.
import os
import pandas as pd
import numpy as np
import pickle
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

# Set globals.
PARENTDIR = os.path.dirname(os.path.realpath(__file__))
DATADIR = os.path.join(PARENTDIR, "../data/raw")
MODELDIR = os.path.join(PARENTDIR, "../models")


# HELPER FUNCTIONS ############################################################
def datetime_to_unix(input):
    return input.astype("datetime64[s]").astype("int")


def load_file_as_dataframe(filename):
    with open(os.path.join(DATADIR, filename), "r") as f:
        data = pd.read_csv(f)
        return data


def save_model_to_file(model, filename):
    output_filename = os.path.join(MODELDIR, filename)
    with open(output_filename, "wb") as f:
        pickle.dump(model, f)


# MAIN ########################################################################
def main():
    # Pull in the necessary data.
    trip_delay_df = load_file_as_dataframe("TRIP_DELAYS.csv")

    # Filter out records with NaN inputs or outputs.
    filtered_trip_delay_df = trip_delay_df.dropna(subset=["TIMESTAMP", "DELAY"])
    print(
        f"{len(trip_delay_df['TIMESTAMP']) - len(filtered_trip_delay_df['DELAY'])} NA records removed."
    )

    # Subset features (inputs) and response (outputs).
    features = filtered_trip_delay_df["TIMESTAMP"].to_numpy()
    response = filtered_trip_delay_df["DELAY"].to_numpy()

    # Transform features into a numeric value for easier use.
    transformed_features = np.apply_along_axis(datetime_to_unix, 0, features)

    # Split the data into training and testing sets.
    features_train, features_test, response_train, response_test = train_test_split(
        transformed_features, response, test_size=0.2, random_state=777
    )

    # Feed training data into the model.
    model = LinearRegression().fit(features_train.reshape(-1, 1), response_train)

    # Spit out predictions.
    preds = model.predict(features_test.reshape(-1, 1))

    # Evaluate the model. Remember, a low MSE is good, and an R2 of 1.0 is good.
    print("Mean squared error: %.2f" % mean_squared_error(response_test, preds))
    print("Coefficient of determination: %.2f" % r2_score(response_test, preds))

    # Save model to file.
    save_model_to_file(model, "linear_regression.pickle")


if __name__ == "__main__":
    main()
