from urllib import request

import click
import pandas as pd
from sqlalchemy import create_engine


@click.command()
@click.option("--user", required=True, help="User name for Postgres")
@click.option("--password", required=True, help="Password for Postgres")
@click.option("--host", required=True, help="Host for Postgres")
@click.option("--port", required=True, help="Port for Postgres")
@click.option("--db", required=True, help="Database name for Postgres")
@click.option(
    "--table_name",
    required=True,
    help="Name of the table where we will write the results to",
)
@click.option("--url", required=True, help="URL of the csv file")
def main(user, password, host, port, db, table_name, url):
    csv_name = "taxi_zone_lookup.csv"
    print(f"Downloading {url} to {csv_name}...")
    request.urlretrieve(url, csv_name)
    print("Download finished.")

    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")

    df = pd.read_csv(csv_name)

    print(f"Inserting data into table '{table_name}'...")
    df.to_sql(name=table_name, con=engine, if_exists="replace")

    print(f"Finished! Inserted {len(df)} rows.")


if __name__ == "__main__":
    main()
