"""
Pulls data from the Transportation Hub down locally.

- jrgarrar
"""

# SETUP #######################################################################
# Import libraries.
import os
import snowflake.connector
from snowflake.connector import *

# Set globals.
PARENTDIR = os.path.dirname(os.path.realpath(__file__))
DATADIR = os.path.join(PARENTDIR, "../data")
DATABASE = "TRANSPORTATION_HUB.HUB"
WAREHOUSE = "COMPUTE_WH"
HOST = "szb57928.prod3.us-west-2.aws"
TABLES = [
    "AGENCIES",
    "ROUTES",
    "ROUTE_SHAPES",
    "STOPS",
    "STOP_SCHEDULE",
    "STOP_TIMES",
    "TRIPS",
    "TRIP_DELAYS",
    "VEHICLES",
    "VEHICLE_POSITIONS",
]


# MAIN ########################################################################
def main():
    # Connect to Snowflake.
    con = snowflake.connector.connect(
        user=os.environ["PIPE_USER"],
        password=os.environ["PIPE_PW"],
        account=HOST,
    )
    cur = con.cursor()

    # Specify warehouse
    cur.execute(f"USE WAREHOUSE {WAREHOUSE}")

    # Load each table in the tables list.
    for table in TABLES:
        # Pull data.
        cur.execute(f"SELECT * FROM {DATABASE}.{table}")
        table_data = cur.fetch_pandas_all()

        # Write to file.
        table_data.to_csv(os.path.join(DATADIR, f"{table}.csv"), index=False)


if __name__ == "__main__":
    main()
