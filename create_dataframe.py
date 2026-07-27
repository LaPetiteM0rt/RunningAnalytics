import os
import sqlalchemy as sa
from dotenv import load_dotenv

def create_dataframe():
    load_dotenv()

    database_url = os.environ["DATABASE_URL"]

    engine = sa.create_engine(database_url)

    metadata = sa.MetaData()

    run_table = sa.Table(
        "run",
        metadata,
        sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=False),
        sa.Column("start_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("distance", sa.Float, nullable=False),
        sa.Column("duration", sa.Float, nullable=False),
        sa.Column("total_elevation_gain", sa.Float),
        sa.Column("average_speed", sa.Float, nullable=False),
        sa.Column("max_speed", sa.Float, nullable=False),
        sa.Column("average_watts", sa.Float),
        sa.Column("max_watts", sa.Float),
        sa.Column("weighted_average_watts", sa.Float),
        sa.Column("kilojoules", sa.Float),
        sa.Column("average_heartrate", sa.Float),
        sa.Column("max_heartrate", sa.Float),
        sa.Column("elev_high", sa.Float),
        sa.Column("elev_low", sa.Float),
        sa.Column("suffer_score", sa.Float),
    )

    metadata.create_all(engine)