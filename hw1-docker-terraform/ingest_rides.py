from time import time
from urllib import request

import click
import pandas as pd
import pyarrow.parquet as pq
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
@click.option("--url", required=True, help="URL of the data file")
def main(user, password, host, port, db, table_name, url):
    if url.endswith(".csv.gz"):
        file_name = "output.csv.gz"
    elif url.endswith(".parquet"):
        file_name = "output.parquet"
    else:
        file_name = "output.file"

    print(f"Downloading {url} to {file_name}...")
    request.urlretrieve(url, file_name)
    print("Download finished.")

    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")

    if file_name.endswith(".parquet"):
        parquet_file = pq.ParquetFile(file_name)
        batches = parquet_file.iter_batches(batch_size=100000)

        try:
            batch = next(batches)
        except StopIteration:
            print("Empty file")
            return

        df = batch.to_pandas()

        df.head(n=0).to_sql(name=table_name, con=engine, if_exists="replace")

        df.to_sql(name=table_name, con=engine, if_exists="append")
        print("Inserted first chunk...")

        for batch in batches:
            t_start = time()

            df = batch.to_pandas()
            df.to_sql(name=table_name, con=engine, if_exists="append")

            t_end = time()
            print(f"Inserted another chunk, took {t_end - t_start:.3f} seconds")

    else:
        df_iter = pd.read_csv(file_name, iterator=True, chunksize=100000)
        df = next(df_iter)

        df.head(n=0).to_sql(name=table_name, con=engine, if_exists="replace")
        df.to_sql(name=table_name, con=engine, if_exists="append")

        while True:
            try:
                t_start = time()
                df = next(df_iter)
                df.to_sql(name=table_name, con=engine, if_exists="append")
                t_end = time()
                print("Inserted another chunk...")
            except StopIteration:
                break

    print("Finished ingesting data into the postgres database")


if __name__ == "__main__":
    main()
